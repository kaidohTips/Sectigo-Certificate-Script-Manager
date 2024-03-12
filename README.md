<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPLv3][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager">
    <img src="lib/images/SCSM_logo.png" alt="Logo">
  </a>

  <h3 align="center">Sectigo Certificate Script Manager</h3>

  <p align="center">
    A tool that use the SECTIGO API to manage your certificates !
    <br />
    <a href="https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager#Usage"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager#Demo">View Demo</a>
    ·
    <a href="https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/issues">Report Bug</a>
    ·
    <a href="https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">Demo</a>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


## Demo


https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/assets/77806690/8cc35781-07fe-4b7f-a45d-dd7a27677deb


<!-- ABOUT THE PROJECT -->
##  🧪 About The Project

As a DevSecOps enthusiast, it's my job to keep the vibes high and maintain the sites in my infrastructure.
Since I couldn't find any tools that vibed with what I wanted for handling certificates via the Sectigo API, I decided to create my own cool tool.

Please note that I've omitted a substantial portion of the main code for GDPR reasons, so fill free to  <a href="https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/issues">Request Feature  </a> 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### 🎨 Built With

[![python][python-shield]][python-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## 🔧 Getting Started

First of all, **Make sure to be at least MRAO and be sure that your account is not disabled.**.

The primary administrator privileges and restrictions are divided as follows:

* MRAO administrator — A Master Registration Authority Officer (MRAO) administrator can make changes across all organizations and departments in an enterprise account without any restrictions.

* RAO administrator — A Registration Authority Officer (RAO) administrator can perform operations on specific organizations and departments and for specific certificate types.

* DRAO administrator — A Department Registration Authority Officer (DRAO) can only perform operations on specific departments and for specific certificate types.


### 📦️ Prerequisites

* Administrator sectigo account as I said above.
* Poetry already setup. See [Poetry Installation](https://python-poetry.org/docs/#installation)
* Python 3.6 or above
* You must have an .env file at the 

### 🚀 Installation

1. Clone the repo
   ```sh
   git clone https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager.git &&
   cd Sectigo-Certificate-Script-Manager
   ```
2. Install the dependencies via Poetry
   ```sh
   poetry install
   ```
3. Enjoy !
   ```sh
   python3 scsm.py info yoursite@domain.com
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE -->
## 📌 Usage

At this point, you can:

| Command    | Description                                |
|------------|--------------------------------------------|
| renew      | Renew the certificate                       |
| info       | Display information of the current certificate |
| download   | Download certificates (x509CO, x509IOR, and x509co) |
| create     | Create a certificate                        |
| update     | Update a certificate                        |



_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## 🔖Roadmap

- [x] Add 'update' command.
- [ ] Add 'deploy' command - CI/CD Pipeline to automatically deploy the certificate in your web server.
- [ ] Add client certificate management.
- [ ] ?

See the [open issues](https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## 💚 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a ✨!!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## 📝 License

Distributed under the GPLv3 License. See [![GPLv3][license-shield]][license-url] for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## 🧑‍💻 Contact

KaidohTips - kaidohTips@protonmail.com 

Project Link: [SCSM](https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## 🎉 Acknowledgments

* [Sectigo API](https://www.sectigo.com/knowledge-base/detail/Sectigo-Certificate-Manager-SCM-REST-API/kA01N000000XDkE)
* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[python-shield]: https://img.shields.io/badge/python--white?style=for-the-badge&logo=python&label=python&color=yellow
[python-url]: https://python.org
[contributors-shield]: https://img.shields.io/github/contributors/kaidohTips/Sectigo-Certificate-Script-Manager.svg?style=for-the-badge
[contributors-url]: https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/kaidohTips/Sectigo-Certificate-Script-Manager.svg?style=for-the-badge
[forks-url]: https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/network/members
[stars-shield]: https://img.shields.io/github/stars/kaidohTips/Sectigo-Certificate-Script-Manager.svg?style=for-the-badge
[stars-url]: https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/stargazers
[issues-shield]: https://img.shields.io/github/issues/kaidohTips/Sectigo-Certificate-Script-Manager.svg?style=for-the-badge
[issues-url]: https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/issues
[license-shield]: https://img.shields.io/github/license/kaidohTips/Sectigo-Certificate-Script-Manager.svg?style=for-the-badge
[license-url]: https://github.com/kaidohTips/Sectigo-Certificate-Script-Manager/blob/master/LICENSE
