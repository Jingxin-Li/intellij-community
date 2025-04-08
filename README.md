# IntelliJ IDEA Community Edition

[![official JetBrains project](http://jb.gg/badges/official.svg)](https://github.com/JetBrains/.github/blob/main/profile/README.md) [![Build status](https://github.com/JetBrains/intellij-community/workflows/IntelliJ%20IDEA/badge.svg)](https://github.com/JetBrains/intellij-community/actions/workflows/IntelliJ_IDEA.yml)

## Overview

IntelliJ IDEA Community Edition is a powerful, open-source integrated development environment (IDE) for Java and other JVM languages, with extensions for many other languages. Developed by JetBrains, it provides intelligent code assistance and robust refactoring tools, making development more productive and enjoyable.

This IDE serves as the foundation for the IntelliJ Platform, which powers many other JetBrains IDEs like PyCharm, WebStorm, and Android Studio.

### Key Features

- **Intelligent Code Assistance**: Smart code completion, on-the-fly error detection, and quick-fixes
- **Powerful Refactoring Tools**: Safe and automated code restructuring
- **Built-in Developer Tools**: Debugger, test runner, terminal, and version control integration
- **Framework Support**: Built-in support for Java EE, Spring, Gradle, Maven, and more
- **Plugin Ecosystem**: Extensible with thousands of plugins from the JetBrains Marketplace

## Installation

### System Requirements

- **RAM**: 2 GB minimum, 8 GB recommended
- **Disk Space**: 2.5 GB minimum, 8 GB recommended
- **Operating System**:
  - Windows 8 or later
  - macOS 10.14 or later
  - Linux with GNOME or KDE desktop

### Installation Methods

#### Method 1: Download and Install

1. Download the installer from the [JetBrains website](https://www.jetbrains.com/idea/download/)
2. Run the installer and follow the installation wizard
3. Launch IntelliJ IDEA from your applications menu or desktop shortcut

#### Method 2: Using a Package Manager

**On macOS (using Homebrew)**:
```bash
brew install --cask intellij-idea-ce
```

**On Linux (using Snap)**:
```bash
sudo snap install intellij-idea-community --classic
```

**On Windows (using Chocolatey)**:
```bash
choco install intellij-idea-community
```

#### Method 3: Building from Source

If you prefer to build from source, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/JetBrains/intellij-community.git
   cd intellij-community
   ```

2. On Windows, set required git configs:
   ```bash
   git config --global core.longpaths true
   git config --global core.autocrlf input
   ```

3. Get additional Android modules:
   - On Linux/macOS: `./getPlugins.sh`
   - On Windows: `getPlugins.bat`

4. Build the project using IntelliJ IDEA:
   - Open the project in IntelliJ IDEA
   - Build the project via **Build | Build Project**

5. To build installation packages:
   ```bash
   ./installers.cmd
   ```

For detailed build instructions, see the [Building from Source](#building-from-source) section below.

## Usage

### Creating a New Project

1. Launch IntelliJ IDEA
2. Select **New Project** from the welcome screen
3. Choose a project type (Java, Kotlin, etc.)
4. Configure project settings and click **Create**

### Opening an Existing Project

1. Launch IntelliJ IDEA
2. Select **Open** from the welcome screen
3. Navigate to your project directory and select it
4. Click **OK** to open the project

### Basic Code Editing

- **Code Completion**: Press `Ctrl+Space` (Windows/Linux) or `⌃Space` (macOS)
- **Quick Documentation**: Press `Ctrl+Q` (Windows/Linux) or `F1` (macOS)
- **Go to Declaration**: Press `Ctrl+B` (Windows/Linux) or `⌘B` (macOS)
- **Find Usages**: Press `Alt+F7` (Windows/Linux) or `⌥F7` (macOS)

### Running and Debugging

- **Run Application**: Press `Shift+F10` (Windows/Linux) or `⌃R` (macOS)
- **Debug Application**: Press `Shift+F9` (Windows/Linux) or `⌃D` (macOS)
- **Set Breakpoint**: Click in the gutter or press `Ctrl+F8` (Windows/Linux) or `⌘F8` (macOS)

## Project Structure

The IntelliJ Platform codebase is organized around several core systems:

- **platform/**: Contains the core platform code
  - **platform/core-api/**: Core APIs used throughout the codebase
  - **platform/platform-api/**: Platform-level APIs
  - **platform/platform-impl/**: Implementation of platform functionality
  - **platform/lang-api/**: Language-agnostic APIs for code processing
  - **platform/lang-impl/**: Implementation of language processing functionality

- **java/**: Java-specific implementation
  - **java/java-psi-api/**: Java Program Structure Interface (PSI) API
  - **java/java-psi-impl/**: Implementation of Java PSI
  - **java/java-impl/**: Java-specific IDE features

- **plugins/**: Contains various plugins bundled with the IDE
  - **plugins/maven/**: Maven integration
  - **plugins/kotlin/**: Kotlin language support
  - **plugins/gradle/**: Gradle integration

## Building from Source

### Prerequisites

- JetBrains Runtime 17 (without JCEF)
- IntelliJ IDEA 2023.2 or newer
- At least 8GB of RAM

### Build Steps

1. Open the project in IntelliJ IDEA
2. Make sure JetBrains Runtime 17 is set as the project SDK
3. If the Maven plugin is disabled, add the path variable "MAVEN_REPOSITORY" pointing to `<USER_HOME>/.m2/repository`
4. Build the project via **Build | Build Project**

### Building Installation Packages

Run the `installers.cmd` command in the project root directory:

```bash
# Build for current OS only
./installers.cmd -Dintellij.build.target.os=current

# Build incrementally
./installers.cmd -Dintellij.build.incremental.compilation=true
```

### Dockerized Build Environment

To build installation packages inside a Docker container:

```bash
docker run --rm -it --user "$(id -u)" --volume "${PWD}:/community" "$(docker build --quiet . --target intellij_idea)"
```

## Running IntelliJ IDEA

To run the IntelliJ IDEA built from source, choose **Run | Run** from the main menu. This will use the preconfigured run configuration "**IDEA**".

To run tests on the build, apply these setting to the **Run | Edit Configurations... | Templates | JUnit** configuration tab:
  * Working dir: `<IDEA_HOME>/bin`
  * VM options: 
    * `-ea` 

## Running Tests in CI/CD Environment

To run tests outside of IntelliJ IDEA, run the `tests.cmd` command in the project root directory:

```bash
# Build incrementally
./tests.cmd -Dintellij.build.incremental.compilation=true

# Run a specific test
./tests.cmd -Dintellij.build.test.patterns=com.intellij.util.ArrayUtilTest
```

## Contributing

We welcome contributions to IntelliJ IDEA Community Edition! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For more information, see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

IntelliJ IDEA Community Edition is licensed under the Apache License, Version 2.0. See the [LICENSE.txt](LICENSE.txt) file for details.

## Resources

- [Official Website](https://www.jetbrains.com/idea/)
- [Documentation](https://www.jetbrains.com/help/idea/discover-intellij-idea.html)
- [Plugin Development](https://plugins.jetbrains.com/docs/intellij/welcome.html)
- [Issue Tracker](https://youtrack.jetbrains.com/issues/IDEA)
- [Community Forum](https://intellij-support.jetbrains.com/hc/en-us/community/topics)
