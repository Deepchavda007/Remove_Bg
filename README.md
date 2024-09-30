<p>
  <div align="center">
      <a href="https://angular.io">
        <img
          src="https://angular.io/assets/images/logos/angular/angular.svg"
          alt="Angular Logo"
          width="300"
          height="300"
        />
      </a>
      <a href="https://www.python.org">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/1/1f/Python_logo_01.svg"
          alt="Python Logo"
          width="300"
          height="300"
        />
      </a>
  </div>
</p>



# Remove Background Image

This project allows users to upload an image, which is processed using a Python backend to remove the background, and then the final image is available for download.

## Project Repo

- Remove Bg (Angular/ Node js/ Python): [https://github.com/Deepchavda007/Remove_Bg](https://github.com/Deepchavda007/Remove_Bg)
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
3. The Python backend processes the image to remove the background using deep learning.
4. The processed image is returned to the frontend for download.

Follow the steps in the [Python Backend Setup](https://github.com/Deepchavda007/Remove_Bg/blob/main/python_backend/README.md) for setting up the Python environment.

## Git Setup

### Cloning the repository

First, clone this repository:

```bash
git clone git@github.com:Deepchavda007/Remove_Bg.git
```

or using https:

```bash
git clone https://github.com/Deepchavda007/Remove_Bg.git
```

Install dependencies:

```bash
npm install
```

### Start development server

Finally, start the development server:

```bash
npm start
```

## Demo : 



https://github.com/user-attachments/assets/76fea35b-bf96-4632-a257-d2b92ee633f2



## Contribution
<a href="https://github.com/Deepchavda007/Remove_Bg/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Deepchavda007/Remove_Bg" />
</a>
