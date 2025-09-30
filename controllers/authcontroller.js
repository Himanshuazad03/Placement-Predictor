const bcrypt = require("bcrypt");
const User = require("../models/user_model");
const jwt = require('jsonwebtoken')
const {generateToken} = require("../utils/generateToken")



module.exports.registerUser = async (req, res) => {
  try {

    const { name, email, password } = req.body;


    // check if user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res
        .status(400)
        .json({ error: "Email already registered", errorField: "email" });
    }

    // hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // save user
    const newUser = new User({
      name: name,
      email,
      password: hashedPassword,
    });

      await newUser.save();
       return res.status(201).json({ ok: true });

    // res.render("/");
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
}

module.exports.loginUser = async function(req,res){
    const { email, password } = req.body;

    let user = await User.findOne({email: email})
    
    if (!user) {
      return res.status(400).json({ error: "Email not registered", errorField: "email" });
    }
  //validate email/phone
  if (!email || email.trim() === "") {
    return res.status(400).json({ error: "Enter your email", errorField: "email" });
  }
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!(emailRegex.test(email))) {
    return res.status(400).json({ error: "Invalid email", errorField: "email" });
  }

  // validate password
  if (!password || password.trim() === "") {
    return res.status(400).json({ error: "Enter Password", errorField: "password" });
  }
 

  bcrypt.compare(password, user.password, (err,result)=>{
    if(result)
    {
        
       let token = generateToken(user);
        res.cookie("token", token, {
      httpOnly: true,
      sameSite: "lax", // ensures it sends with redirect
      maxAge: 24 * 60 * 60 * 1000, // 1 day

  });
        return res.status(201).json({ ok: true });
    }
    else{
       return res.status(400).json({ error: "Password is incorrect", errorField: "password" })
    }
  })
  
}
