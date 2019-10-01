const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')
const dotenv = require('dotenv')
const fs = require('fs')
const path = require('path')
const os = require('os')
dotenv.config()
const app = express()
app.use(bodyParser.urlencoded({ extended: true }))
app.use(cors({ origin: 'http://localhost:3000' }))
// Set Request Size Limit
app.use(bodyParser.json({ limit: '200mb', extended: true }))
app.use(bodyParser.urlencoded({ limit: '200mb', extended: true }))
// Talk to amazon
const AWS = require('aws-sdk')
AWS.config.update({
  accessKeyId: process.env.AWS_ACCESS_KEY,
  secretAccessKey: process.env.AWS_ACCESS_SECRET
})

const s3 = new AWS.S3()
const Bucket = 'model-converter532f66f4e234418c985ae1d5bc842f55-dev'

const configureRoutes = require('./routes')
// for running commands
const exec = require('child_process').exec
// Do Port (8000 for dev - 3000 for prod)
const usePort = process.env.DEV_PORT || 3000
// Payment stuffs
configureRoutes(app)

// API process stuffs
app.post('/reform', async (req, res) => {
  const { Key, folder, fileName } = req.body
  const file = await s3.getObject({ Bucket, Key }).promise()

  const localPath = path.join(os.tmpdir(), folder)
  fs.mkdir(localPath, { recursive: true }, console.error)
  fs.mkdir(path.join(localPath, 'results'), { recursive: true }, console.error)
  const localFile = path.join(localPath, fileName)
  fs.writeFile(localFile, Buffer.from(file.Body), console.error)
  console.log('File placed', localFile)

  // Perform action on file
  exec(
    `converters/zip_file.sh ${localPath} ${fileName}`,
    {
      encoding: 'utf-8'
    },
    error => {
      if (error) {
        console.log(error)
        res.send({ success: false })
      }

      console.log('Zip created')

      const filePath = path.join(localPath, 'results', 'result.zip')
      const params = {
        Bucket,
        Body: filePath,
        Key: `public/results/${folder}/results.zip`
      }

      s3.upload(params, function(err, data) {
        //handle error
        if (err) {
          console.log('Error', err)
        }

        //success
        if (data) {
          console.log('Uploaded in:', data.Location)
        }
      })
    }
  )
})

// Upload stuffs - NOT BEING USED!
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
  if (!req.body.file) {
    res.status(400).send('No file sent')
    console.log('no file')
    return
  }
  const { file, content, info, folder, fileName } = req.body
  const localPath = path.join(os.tmpdir(), folder)
  fs.mkdir(localPath, { recursive: true }, console.error)
  fs.mkdir(path.join(localPath, 'results'), { recursive: true }, console.error)
  const localFile = path.join(localPath, fileName)
  fs.writeFile(localFile, Buffer.from(req.body.file.data), console.error)
  console.log('File placed', localFile)

  // Perform action on file
  exec(
    `converters/zip_file.sh ${localPath} ${fileName}`,
    {
      encoding: 'utf-8'
    },
    error => {
      if (error) {
        console.log(error)
        res.send({ success: false })
      }

      console.log('Zip created')
      const fileContents = fs.readFileSync(
        path.join(localPath, 'results', 'result.zip')
      )

      res.send({
        success: true,
        fileName: 'result.zip',
        fileBody: Buffer.from(fileContents, 'utf8')
      })
    }
  )
})

app.listen(usePort, error => {
  if (error) throw error
  console.log('API running on port ' + usePort)
})
