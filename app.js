const express = require('express');
const app = express();
const path = require('path')
const config = require('config')
const mongoose = require('mongoose')
const bcrypt = require('bcrypt')
const expressSession = require("express-session");
const {registerUser, loginUser} = require("./controllers/authcontroller")
const isAuthenticated = require('./Middleware/isAuthenticated')
const cookieParser = require('cookie-parser');
const isLoggedin = require('./Middleware/isLoggedin')
const { spawn } = require("child_process");

require('dotenv').config();
app.set("view engine", "ejs");
app.use(express.json());
app.use(express.urlencoded({extended: true}));
app.use(express.static(path.join(__dirname,"public")));
app.use(cookieParser())
app.use(isAuthenticated)


const userModel = require("./models/user_model");


async function connectDB() {
  try {
    const mongoURI = config.get("MONGO_URI");

    await mongoose.connect(`${mongoURI}/placement`);
  } catch (err) {
    console.error("❌ MongoDB connection failed:", err);
    process.exit(1);
  }
}

connectDB();

app.use(
    expressSession({
        resave: false,
        saveUninitialized: false,
        secret: process.env.EXPRESS_SESSIONS_SECRET,
    })
)


app.get("/", (req,res)=>{
     if (req.user) {
    // Already logged in, redirect to predict page
    return res.redirect("/skill");
  }
    res.render("home", {currentPage : "home", user: req.user});
})

app.get("/skill", isLoggedin, (req,res)=>{
    res.render("skill", {currentPage : "skill", user: req.user})
})

app.post("/predict", isLoggedin, (req, res) => {
  const formData = req.body;

  const python = spawn("python", ["./predict.py", JSON.stringify(formData)]);
  let output = "";

  python.stdout.on("data", (data) => {
    output += data.toString(); // collect all stdout chunks
  });


  python.stderr.on("data", (err) => {
    console.error("Python error:", err.toString());
  });

  python.on("close", (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: "Python script failed" });
    }
    const probability = parseFloat(output.trim());
    res.json({ probability }); // send exact value to frontend
  });
});

app.post("/skill-predict", isLoggedin, (req, res) => {
  const data = req.body;

  const python = spawn("python", ["./skill_predict.py", JSON.stringify(data)]);
  
  python.stdout.on("data", (output) => {
    res.send(output.toString().trim());
  });
  

  python.stderr.on("data", (err) => {
    console.error(err.toString());
    res.status(500).send("Error in prediction");
  });

});

app.get("/developer", (req, res)=>{
  res.render("developer", {currentPage : "developer", user: req.user})
})

app.get("/home", (req, res)=>{
  res.render("home", {currentPage : "home", user: req.user})
})

app.get("/login", (req,res)=>{
    res.render("login",{currentPage : "login", user: req.user})
})

app.get("/signup", (req,res)=>{
    res.render("signup",{currentPage: "signup", user: req.user});
})

app.get("/predict", isLoggedin, (req,res)=>{
    res.render("predict", {currentPage: "predict", user: req.user})
})

app.post("/register", registerUser)


app.post("/login", loginUser)

app.get("/logout", (req,res)=>{
  res.clearCookie("token")
  res.redirect("/login")
})

app.get("/privacy", (req,res)=>{
  res.render("privacy", {currentPage: "privacy", user: req.user});
})

app.get("/terms", (req,res)=>{
  res.render("terms", {currentPage: "terms", user: req.user});
})

app.listen(3000);
