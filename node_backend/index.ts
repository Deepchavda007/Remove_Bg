import express, { Express, Request, Response, NextFunction } from "express";
import multer, { FileFilterCallback, MulterError } from "multer";
import axios from 'axios';
import path from 'path';
import dotenv from "dotenv";
import fs from 'fs';
dotenv.config();
import cors from "cors";
import compression from 'compression';

const app: Express = express();
const port = process.env.PORT || 3000;
app.use(express.json());
app.use(compression({ level: 9 }));
app.use(require('express-status-monitor')());

// Ensure the uploads directory exists
const uploadsDir = 'uploads';
if (!fs.existsSync(uploadsDir)){
    fs.mkdirSync(uploadsDir);
}

// Serve static files from the uploads directory
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Enable CORS for all routes
app.use(cors({
  origin: "*",
}));

// Function to generate a 6-digit unique image ID
const generateImageId = (): string => {
  return Math.floor(100000 + Math.random() * 900000).toString(); // Generates a 6-digit number
};

// Configure Multer to upload only image files
const storage = multer.diskStorage({
  destination: function (req: Request, file: Express.Multer.File, cb: (error: Error | null, destination: string) => void) {
      cb(null, 'uploads/'); // Destination folder for uploaded images
  },
  filename: function (req: Request, file: Express.Multer.File, cb: (error: Error | null, filename: string) => void) {
      const imageId = generateImageId(); // Generate the 6-digit ID
      const fileName = `image-${imageId}${path.extname(file.originalname)}`; // Construct the filename
      cb(null, fileName); // Save the file with the new unique name
  }
});

// File filter to accept only image files
const fileFilter = (req: Request, file: Express.Multer.File, cb: FileFilterCallback) => {
  const allowedTypes = /jpeg|jpg|png|gif/;
  const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
  const mimetype = allowedTypes.test(file.mimetype);

  if (extname && mimetype) {
      cb(null, true);
  } else {
      cb(new Error('Only image files are allowed!'));
  }
};

const upload = multer({
  storage: storage,
  fileFilter: fileFilter
});

// Route to handle image upload and API call to remove background
app.post('/upload', upload.single('image'), async (req: Request, res: Response, next: NextFunction) => {
  try {
      // Check if file exists
      if (!req.file) {
          return res.status(400).json({ message: 'No image uploaded!' });
      }

      const imageId = generateImageId(); // Generate a unique image ID
      const imageUrl = `https://594d-103-251-19-88.ngrok-free.app/uploads/${req.file.filename}`; // Generate image URL

      // Make POST request to the external API
      const apiResponse = await axios.post('http://127.0.0.1:8000/remove_bg', {
          image_url: imageUrl,
          image_id: imageId,
      });

      // Respond to the frontend with the result from the external API
      res.json({
          message: 'Image uploaded successfully',
          fileName: req.file.filename,
          filePath: imageUrl,
          removeBgApiResponse: apiResponse.data, // Send back the response from the background removal API
      });
  } catch (error) {
      next(error);
  }
});

// Error handling middleware for multer
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err);
  if (err instanceof MulterError) {
      res.status(500).json({ error: err.message });
  } else if (err) {
      res.status(500).json({ error: err.message });
  }
});

app.use('/', require("./routes/routes"));

app.listen(port, async () => {
  console.log(`[server]: Server is running at http://localhost:${port}`);
});
