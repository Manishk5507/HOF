const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const cors = require('cors');
var expressSession = require("express-session");
var jwt_decode = require('jwt-decode');


const app = express();
const PORT = process.env.PORT || 3000;

// Middleware

app.use(
  expressSession({
    resave: false,
    saveUninitialized: false,
    secret: "hello I am here!!",
  })
);
app.use(bodyParser.json());
app.use(cookieParser());

app.use(cors({
  origin: '*', // Allow requests from any origin
  credentials: true, // Allow cookies to be sent and received from the client-side
}));


app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*'); // Allow requests from any origin
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    if (req.method === 'OPTIONS') {
      res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE');
      return res.status(200).json({});
    }
    next();
  });

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/signup', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Schema and Model
const userSchema = new mongoose.Schema({
  username: String,
  email: {
    type: String,
    unique: true,
  },
  password: String,
  about:{
    type:String,
    default:""
  }
});

const User = mongoose.model('User', userSchema);

// Routes

// Serve static files from the 'public' directory
// app.use(express.static('web'));

// Redirect '/' route to 'index.html' file in the 'public' directory
app.get('/', (req, res) => {
  res.send(token);
});


// Signup
app.post('/signup', async (req, res) => {
  try {
    const { username, email, password } = req.body;

    // Input validation
    if (!username || !email || !password) {
      return res.status(400).json({ error: 'Please provide all fields' });
    }

    // Password hashing
    const hashedPassword = await bcrypt.hash(password, 10);

    const existingUser = await User.findOne({ email }).populate();

    if (existingUser) {
      return res.status(400).json({ error: 'User already exists' });
    }

    const newUser = new User({ username, email, password: hashedPassword });
    await newUser.save();

    // Generate JWT token
    const token = jwt.sign({ userId: newUser._id }, 'secretkey', { expiresIn: '1h' });


    // Set JWT token as an HTTP cookie in the response
    // res.cookie('token', token, { path: 'http://127.0.0.1:5500/profile.html' });

   
    res.status(201).json({ message: 'User created successfully', token:token,user:username, email:email});
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});


// Login
app.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const passwordMatch = await bcrypt.compare(password, user.password);

    if (!passwordMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Generate JWT token
    const token = jwt.sign({ userId: user._id }, 'secretkey', { expiresIn: '1h' });

    //res.cookie('token', token, { path: 'http://127.0.0.1:5500/profile.html' });
    
    // res.status(200).json({ token });
    res.status(200).json({ message: 'Login successful' ,token:token,user:user.username, email:user.email});
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Middleware for verifying JWT token
const verifyToken = (req, res, next) => {
  const token = req.cookies.token;

  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  jwt.verify(token, 'secretkey', (err, decoded) => {
    if (err) {
      return res.status(401).json({ error: 'Invalid token' });
    }

    req.userId = decoded.userId;
    next();
  });
};

// Protected route example
// Profile route example
app.get('/profile', verifyToken, async (req, res) => {
  try {
    // Find the user based on the user ID extracted from the JWT token
    const user = await User.findById(req.userId);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Return user data including the username
    res.status(200).json({ username: user.username}); // You can include other user data as needed
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

//About route
app.post('/updateAbout', async (req, res) => {
  const aboutText = req.body.about;
  const userEmail = req.body.email; // Assuming email is being sent along with the request

  try {
      // Find user by email
      const user = await User.findOne({ email: userEmail });

      // If user found, update "about" field
      if (user) {
          user.about = aboutText;
          await user.save();
          res.send('About You updated successfully!');
      } else {
          res.status(404).send('User not found');
      }
  } catch (error) {
      console.error('Error updating About You:', error);
      res.status(500).send('Internal Server Error');
  }
});





// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
