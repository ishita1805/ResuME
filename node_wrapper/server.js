require('dotenv').config();
const express = require('express');
const app = express();
const cors = require('cors');
const PORT  =  process.env.PORT || 3001
const deployRoutes = require('./src/routes/deploy')

app.use(express.json());
app.use(cors())

app.use('/deploy',deployRoutes)


app.get('/', async(req,res) => {
   res.send('API Health OK!');
})

// github openapi endpoints: https://api.github.com/
  
app.listen(PORT,() => {
    console.log("Listening on port "+ PORT);
})

