// middleware/isAuthenticated.js
const jwt = require("jsonwebtoken");

function isAuthenticated(req, res, next) {
  const token = req.cookies.token;
  if (!token) {
    req.user = null; // no login, but continue
    return next();
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_KEY);
    req.user = decoded; // attach user info

  } catch (err) {
    req.user = null; // invalid/expired token
  }

  next();
}

module.exports = isAuthenticated;
