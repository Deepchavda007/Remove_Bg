```markdown
<p>
  <div align="center">
      <a href="https://github.com/Deepchavda007/Remove_Bg">
        <img
          src="https://angular.io/assets/images/logos/angular/angular.svg"
          alt="Angular Project"
          width="300"
          height="300"
        />
      </a>
  </div>
</p>

# Remove Background Image - Angular & Node.js Project

This project allows users to upload an image, which is processed using a Python backend to remove the background, and then the final image is available for download.

## Project Repo

- Frontend (Angular): [https://github.com/Deepchavda007/Remove_Bg](https://github.com/Deepchavda007/Remove_Bg)
- Python Backend: [Python Backend Setup](https://github.com/Deepchavda007/Remove_Bg/blob/main/python_backend/README.md)

## Development Setup

### 1. Spartan UI Setup in Angular

To integrate Spartan UI library into the Angular project, follow these steps:

1. Install Spartan UI library:

```bash
npm install @spartan/ui
```

2. Add Spartan UI styles to your global styles file (`src/styles.scss`):

```scss
@import '@spartan/ui/styles';
```

3. Use Spartan components in your Angular templates. For example:

```html
<button hlmBtn (click)="onClick()">Upload Image</button>
```

### 2. Node.js Backend

The backend of the project is built with Node.js to handle the API requests and connect to the Python service for image processing.

To set up the backend:

1. Install dependencies:

```bash
npm install
```

2. Run the Node.js server:

```bash
npm start
```

The Node.js server listens for image upload requests and forwards them to the Python backend for processing.

### 3. Image Processing Flow (Python Backend)

1. The user uploads an image via the Angular frontend.
2. The image is sent to the Node.js server, which forwards the image to the Python backend.
3. The Python backend processes the image to remove the background using machine learning.
4. The processed image is returned to the frontend for download.

Follow the steps in the [Python Backend Setup](https://github.com/Deepchavda007/Remove_Bg/blob/main/python_backend/README.md) for setting up the Python environment.

## Git Setup

There are two branches in the repository:

- `develop` for active development
- `main` official branch used for production releases

### Cloning the repository

First, clone this repository:

```bash
git clone git@github.com:Deepchavda007/Remove_Bg.git
```

or using https:

```bash
git clone https://github.com/Deepchavda007/Remove_Bg.git
```

Check out `develop` or `main` and install dependencies:

```bash
git checkout develop
npm install
```

### Start development server

Finally, start the development server:

```bash
npm start
```

## Contributing

To contribute, create a new branch from the `develop` branch, and use a meaningful branch name with prefixes like `fix/` for bug fixes or `feat/` for new features:

```bash
git checkout -b feat/new-feature-name
```

After making changes, ensure there are no linting errors:

```bash
npm run lint
```

Fix any linting errors:

```bash
npm run lint:fix
```

Format your code using Prettier:

```bash
npm run prettier
```

Commit and push your changes:

```bash
git push
```

Finally, submit a pull request (PR) for review.
```
