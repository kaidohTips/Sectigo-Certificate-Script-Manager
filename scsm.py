#!/usr/bin/python3

"""
  █████████    █████████   █████████  ██████   ██████
 ███░░░░░███  ███░░░░░███ ███░░░░░███░░██████ ██████ 
░███    ░░░  ███     ░░░ ░███    ░░░  ░███░█████░███ 
░░█████████ ░███         ░░█████████  ░███░░███ ░███ 
 ░░░░░░░░███░███          ░░░░░░░░███ ░███ ░░░  ░███ 
 ███    ░███░░███     ███ ███    ░███ ░███      ░███ 
░░█████████  ░░█████████ ░░█████████  █████     █████
 ░░░░░░░░░    ░░░░░░░░░   ░░░░░░░░░  ░░░░░     ░░░░░ 


This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""

import requests
import argparse
import os
from yaspin import yaspin
import json
import sys
import argparse
import subprocess
from dotenv import load_dotenv
from fabric import Connection, task
import pendulum
import time


with yaspin() as sp:
    time.sleep(1)

def GetId(server: str) -> str:
    try:
        response = requests.get("https://cert-manager.com/api/ssl/v1", headers=HEADERS, params={'commonName': server})
        response.raise_for_status()
        return response.json()[0]['sslId'] 
    except Exception as e:
        print("Error",e)

@yaspin(text=f"Binding account to the SECTIGO API ...")
def BindAPI() -> bool:
    try:
        response = requests.get("https://cert-manager.com/api/ssl/v1", headers=HEADERS)
        if response.status_code == 200:
            sp.write("Binding to the sectigo API status : [OK]")
            return True
        sp.write("Binding to the sectigo API status: [FAIL]")
        sp.write("Make sure to check your '.env' file or the state of your account in the Sectigo API")
        return False
    except Exception as e:

        return False

def GetCertificateInfo(server: str) -> dict[str, str]:
    response = requests.get(f"https://cert-manager.com/api/ssl/v1/{GetId(server)}", headers=HEADERS, params={'commonName': server})
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

@yaspin(text=f"Display Certificate Info ...")
def DisplayInfo(server: str) -> dict[str, str]:
    for info_k, info_v in GetCertificateInfo(server).items():
        sp.write(f"{info_k}: {info_v}")
    sp.ok("")

def RenewCertificate(server: str) -> bool:
    """
    Renew the certificate mapped to the design FQDN 
    """
    
    if options.overwrite:
        is_renew = input(str(f"Are you sure to renew the certificate of the server '{server}' ? [y/n]"))
        if is_renew != 'y' or is_renew != 'yes':
            print(f"Renew Abort ... :(")
            sys.exit(1)
    
    r = requests.post(f"https://cert-manager.com/api/renew/{GetId(server)}", headers=HEADERS, params={'commonName': server})
    if r.status_code == 200:
        print(f"The certificate of '{server}' has been renewed '{r.text}'.")
    else:
        print(f"Failed to renew certificate of '{server}'")
        sys.exit(1)


def SaveCertificate(content: bytes, filename: str | os.PathLike) -> None:
    """
    Save the certificate
    """
    with open(filename, 'wb') as file:
        file.write(content)

@yaspin(text=f"Downloading Certificate ...")
def DownloadCerts(server: str, _format: list[str], _path: str | os.PathLike) -> None:
    """
    Format type for certificate:
        - Allowed values: 'x509' - for Certificate (w/ chain)
        - PEM encoded, 'x509CO' - for Certificate only
        - PEM encoded, 'base64' - for PKCS#7
        - PEM encoded, 'bin' - for PKCS#7
        - 'x509IO' - for Root/Intermediate(s) only
        - PEM encoded
        - 'x509IOR' - for Intermediate(s)/Root only
        - PEM encoded, 'pem' - for Certificate (w/ chain)
        - PEM encoded, 'pemco' - for Certificate only
        - PEM encoded, 'pemia' - for Certificate (w/ issuer after)
        - PEM encoded, 'x509R' - for Certificate (w/ chain)
        - PEM encoded, 'pkcs12' - for Certificate and Private key, PKCS#12. base64 is default.
    Download certificate
    """

    TimeOut = 120  # in seconds
    retry_interval = 5  # in seconds also

    start_time = pendulum.now()

    while pendulum.now().diff(start_time).in_seconds() < TimeOut:
        
        if GetCertificateInfo(server)['status'] == "Issued":
            break
    else:
        sp.fail("TimeOut API Down Or there's problem with the status of your certificate")
        sys.exit(1)

    for f in _format:
        response = requests.get(f"https://cert-manager.com/api/ssl/v1/collect/{GetId(server)}", headers=HEADERS, params={'commonName': server, 'format': f })
        cert_name = response.headers.get("Content-Disposition")
        if cert_name:
            cert_name = cert_name.split("filename")[1].strip('="')
        assert cert_name != None
        sp.write(f"Certificate Name: {cert_name}\n\tFormat: {f}")            
        SaveCertificate(response.content, f"{_path}/{cert_name}")
   
    sp.ok("")

@yaspin(text=f"Updating certificate ...")
def UpdateCertificate(server: str, **kwargs : dict) -> None:
    """
    You can update only certificate fields listed in the table below.
    Organization ID, Certificate Profile ID, Term, Common name, CSR, SANs can be edited if a certificate state is one of
        - Requested
        - Declined
        - Rejected
        - Invalid
    """
    if GetId(server):
        payload = {}
        payload['sslId'] = GetId(server)
        
        for key, value in kwargs.items():
            if key in ["orgId", "certTypeId", "term", "commonName", "csr", "subjectAlternativeNames"] and value is not None:
                if GetCertificateInfo(server)['status'] != ['Requested','Declined','Rejected','Invalid']:
                    print(f"Warning ! Status must not be Issued to change: '{key}'")
                else:
                    payload[key] = value                
            else:
                payload[key] = value                
        
        response = requests.put(f"https://cert-manager.com/api/ssl/v1/", headers=HEADERS, json=payload)
        if response.status_code == 200:
            sp.ok("")
        else:
            sp.fail("")

@yaspin(text=f"Creation of RSA Key ...")
def NewKey(server: str, size, csr_path: str | os.PathLike, key_path: str | os.PathLike, term, country: str, city: str, org: str):
    try:
        new_key = subprocess.run(["openssl","req","-new","-newkey",f"rsa:{size}","-nodes","-days", term, "-out", csr_path + server + ".crt","-keyout", key_path + server + ".key", "-subj", f"/C={country}/ST={state}/L={city}/O={org}/CN={server}"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        if new_key.returncode == 0:
            sp.ok(f"RSA Key of {size} created !")
            return csr_path + server + ".crt"
        else:
            sp.fail("")
            sys.exit(1)
            return None
    except Exception as e:
        print("Error",e)    
    

@yaspin(text=f"Creation of Certificate ...")
def CreationCertificate(server: str, size, csr_path: str | os.PathLike, key_path: str | os.PathLike, term, san: list[str], country: str, city: str, org: str) -> None:
	if NewKey(server, size, csr_path, key_path, term, country, city, org):
		with open(csr_path + server + ".crt", 'r') as f:
			csr_data = f.read()
			r = requests.post("https://cert-manager.com/api/ssl/v1/enroll", headers=HEADERS, json={'orgId': os.environ.get("SECTIGO_ORG_ID"), 'certType': os.environ.get("SECTIGO_CERT_TYPE_ID"), 'csr': csr_data, 'subjAltNames': ",".join(san) , 'term': term, 'comments': f'Creation of {server} certificate via API','externalRequester':''})
			print(r.text)
			if r.status_code == 200:
				sp.ok("Certificate created!")
			else:
				sp.fail("")

if __name__ == "__main__":
    load_dotenv()

    HEADERS = {
            'login': os.environ.get("SECTIGO_USER"),
            'Content-Type': 'application/json;charset=utf-8',
            'customerUri': os.environ.get("SECTIGO_CUSTOMER_URI"),
            'password': os.environ.get("SECTIGO_PASS")
        }


    parser = argparse.ArgumentParser(description="Tools to manage certificate issued from SECTIGO",
                                     epilog="@kaidohTips",
                                     formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers()

    parser_bind = subparsers.add_parser("bind",help="test de connectivity with the SECTIGO API")

    parser_renew = subparsers.add_parser("renew",help="Renew the certificate")
    parser_renew.add_argument("fqdn",type=str,metavar="FQDN",help="FQDN to renew",nargs="+")
    parser_renew.add_argument("--overwrite","-o",action="store_true",help="Bypass Prompt")

    parser_info = subparsers.add_parser("info", help="Display information of the current certificate")
    parser_info.add_argument("fqdn",type=str,metavar="FQDN",help="FQDN of the certificate to display",nargs="+")

    parser_download = subparsers.add_parser("download", help="Download certificates (x509CO, x509IOR and x509co)")
    parser_download.add_argument("fqdn", type=str,metavar="Destination Server",help="Server where you want to download the certificate")
    parser_download.add_argument("--format", "-f", type=str, metavar="format",help="Format",default=["x509","x509CO","x509IOR"],nargs="+")
    parser_download.add_argument("--path", "-p", type=str, metavar="DOWNLOAD PATH",help="Path where you'll store your downloaded certificates")

    parser_create = subparsers.add_parser("create",help="Create a certificate")
    parser_create.add_argument("fqdn",type=str,help="FQDN Full Qualified Distingued Name")
    parser_create.add_argument("--size",type=str,help="Size of RSA key",default="4096")
    parser_create.add_argument("orgid",type=str,help="OrgID of your domain",default=os.environ.get("SECTIGO_ORG_ID"))
    parser_create.add_argument("cert_type",type=str,help="CertType ID of your domain",default=os.environ.get("SECTIGO_CERT_TYPE_ID"))
    parser_create.add_argument("--csr_path",type=str,help="Path CRT")
    parser_create.add_argument("--key_path",type=str,help="Path KEY")
    parser_create.add_argument("--term",type=str,help="Term (days)",default="365")
    parser_create.add_argument("--SubjectAlternativeNames","--san",type=list[str],help="Subject Alternatives Names of your certificates")

    parser_update = subparsers.add_parser("update",help="Update a certificate")
    parser_update.add_argument("fqdn", type=str, help="FQDN Full Qualified Distingued Name")
    parser_update.add_argument("--term", type=int, help="Term (in days)")
    parser_update.add_argument("--certTypeId", type=int, help="Certificate Profile ID", nargs="+")
    parser_update.add_argument("--orgId", type=int, help="Organization ID")
    parser_update.add_argument("--commonName", type=str, metavar="COMMON_NAME", help="Certificate common name")
    parser_update.add_argument("--csr", type=str, metavar="CSR", help="Certificate signing request")
    parser_update.add_argument("--externalRequester", type=str, help="External requester emails, comma-separated")
    parser_update.add_argument("--comments", type=str, metavar="REASON", help="Comments", nargs="?")
    parser_update.add_argument("--subjectAlternativeNames","--san", type=list[str], metavar="SUBJECT ALTERNATIVE NAMES", help="Subject alternative names", nargs="+")

    options = parser.parse_args()


    if len(sys.argv) > 1:
        if sys.argv[1] == 'renew':
            RenewCertificate(options.fqdn)

        elif sys.argv[1] == 'bind':
            BindAPI()

        elif sys.argv[1] == 'info':
            DisplayInfo(options.fqdn)

        elif sys.argv[1] == 'download':
            DownloadCerts(options.fqdn,options.format, options.path)

        elif sys.argv[1] == 'update':
            UpdateCertificate(options.fqdn, **vars(options))

        elif sys.argv[1] == 'create':
            CreationCertificate(options.fqdn, options.size, options.csr_path, options.key_path, options.term, options.san, options.country, options.state, options.city)
    else:
        parser.print_help()
