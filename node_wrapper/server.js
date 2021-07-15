require('dotenv').config();
const express = require('express');
const app = express();
const cors = require('cors');
const axios = require('axios');
const PORT  =  process.env.PORT || 3001

app.use(express.json());
app.use(cors())


app.get('/', async(req,res) => {
   res.send('API Health OK!');
})


app.get('/auth', async(req,res) => {
    axios.get('https://www.linkedin.com/oauth/v2/authorization',{
        params:{
            response_type:"code",
            client_id:process.env.ID,
            redirect_uri:'http://localhost:3001/red',
            state:"ybwxpbktwuhcewp0b543238sd",
            scope:'r_liteprofile r_emailaddress'
        }
    })
    .then((resp)=>res.redirect(resp.request.res.responseUrl))
    .catch((er)=>res.json(er));
})

app.get('/red', async(req,res) => {
    axios.post('https://www.linkedin.com/oauth/v2/accessToken',null,{
        params:{
            grant_type:'authorization_code',
            client_id: process.env.ID,
            client_secret: process.env.SECRET,
            redirect_uri:'http://localhost:3001/red',
            code: req.query.code,
        },
        headers: {'Content-Type': 'x-www-form-urlencoded'}
    })
    .then((resp)=>{
        // console.log(resp);
        // res.send(resp.data);
        axios.get('https://api.linkedin.com/v2/me',{
            params:{
                oauth2_access_token: resp.data.access_token,
            }
        })
        .then((resp) => {
            console.log(resp);
            res.json({
                data: resp.data
            })
        })
        .catch((e) => {
            console.log(e);
            res.json({
                e
            })
        })
    })
    .catch((e)=>{
        console.log(e);
        res.json(e);
    })
})

// github openapi endpoints: https://api.github.com/
  
app.listen(PORT,() => {
    console.log("Listening on port "+ PORT);
})

