# Python Devcontainer Environment with Docker

This repository contains a Docker-based development environment for Python projects. It provides a consistent and isolated environment for Python development, ensuring that all team members use the same dependencies and configurations.

## Prerequisites
- Docker: [Install Docker](https://docs.docker.com/get-docker/)
  - In case of windows, please prepare docker environment in wsl2
- Visual Studio Code: [Install VS Code](https://code.visualstudio.com/download)
- docker for windows(mac): [docker for windows](https://docs.docker.com/desktop/install/windows-install/)

### Visual Studio Code Extention Package
- Dev Containers
  - Remote Development with Dev Containers included is also OK.

## Getting Started

1. Clone this repository to your local machine:

    ```bash
    git clone <this repository url>
    ```

2. Navigate to the project directory:

    ```bash
    cd <project_directory>
    ```

3. Enter the required pip package in the `requirements.txt` file in the `.devcontainer` folder
    example:
    ```txt
    numpy==1.26.0
    pandas=>2.2.0
    ```

4. Press `ctrl + shift + p` to select `>Dev Containers: rebuild and reopen in container`

5. Wait a little....

## How to change remote repositories for development

1. Create a new repository on GitHub.

2. In your local environment, use the following command to check the information of the current remote repository:

    ```bash
    git remote -v
    ```

3. Change the remote repository to the new GitHub repository. Use the following command to change the remote URL:

    ```bash
    git remote set-url origin <your_new_github_repository>
    ```

4. Push the changes.

    ```bash
    git push origin main
    ```

    (Or use the branch name corresponding to the `main` branch)

5. Refresh the repository page on GitHub to reflect the changes.

## Directory Structure

The directory structure of this project is as follows:

```
project_root/
│
├── .devcontainer/
│   ├── Dockerfile
│   ├── devcontainer.json
│   └── requirements.txt
│
│── .gitignore
│
│── LICENSE.txt
│── README.md
│
├── other_project_files...
```

- `.devcontainer/`: Contains Docker configuration files.
  - `Dockerfile`: Defines the Docker image for the development environment.
  - `devcontainer.json`: Configuration file for Visual Studio Code Remote Development.
  - `requirements.txt`: File containing Python dependencies for the project.

- `.gitignore`: This file allows you to specify files or directories to exclude from Git tracking.

## Contributing

If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
