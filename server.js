const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')
const dotenv = require('dotenv')
const fs = require('fs')
dotenv.config()
const app = express()
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(cors({ origin: 'http://localhost:3000' }))
const configureRoutes = require('./routes')
// Do Port (8000 for dev - 3000 for prod)
const usePort = process.env.DEV_PORT || 3000
// Payment stuffs
configureRoutes(app)

// Upload stuffs
/*
  body: {
    file: { type: 'Buffer', data: [Array] },
    content: 'image/png',
    info: { types: 'all' },
    folder: 'b57307a1-2315-4239-9508-9d1a75bcbf1c',
    fileName: 'favicon-32x32.png'
  }
*/
app.post('/upload', function(req, res) {
  console.log(req.body)
  if (!req.body.file) {
    res.status(400).send('No file sent')
    console.log('no file')
    return
  }
  fs.writeFile('./test.png', Buffer.from(req.body.file.data), console.error)
})

app.listen(usePort, error => {
  if (error) throw error
  console.log('API running on port ' + usePort)
})
