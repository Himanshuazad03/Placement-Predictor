const jwt = require('jsonwebtoken')

function isLoggedin(req, res, next){
    const token = req.cookies.token

    if(!token)
    {
        return res.redirect("/login")
    }

    try {

        const decode = jwt.verify(token, process.env.JWT_KEY)

        req.user = decode
        next()
        
    } catch (error) {
        return res.redirect("/login")
    }
}

module.exports = isLoggedin