// Load Node modules
var express = require('express');
const ejs = require('ejs');
// Initialise Express
var app = express();
// Render static files
app.use(express.static('public'));

// Set the view engine to ejs
app.set('view engine', 'ejs');

app.set('views', __dirname+'/views');
// Port website will run on
app.listen(3000);



const fs = require('fs');
// Read data from file

let rawdata = fs.readFileSync('data.json');
var data = JSON.parse(rawdata);
let rawdata2 = fs.readFileSync('output.json');
var data2 = JSON.parse(rawdata2);
console.log(data);



app.get('/', function (req, res) {
    res.render('pages/index', {
      data: data,
      data2: data2
    });  
});


app.get('/index.ejs', (req, res) => {
    if (req.query.password === "ABC") { // FIXME need to compare password's hash
      // Add received data to data file
      data.unshift({"first_name":req.query.first_name,"last_name":req.query.last_name,"first_day":req.query.first_day,"last_day":req.query.last_day});
      // Write data to file
      fs.writeFileSync('data.json', JSON.stringify(data), function (err) {if (err) return err;});
      
      // TODO: VIDER LE FICHIER AVANT D'ÉCRIRE
      
      const { exec } = require('child_process');
        console.log("Entered")
              // Executes Python code
                exec("python3.9 exe.py "+JSON.stringify(req.query.first_name)+" "+JSON.stringify(req.query.last_name)+" "+JSON.stringify(req.query.first_day)+" "+JSON.stringify(req.query.last_day), (err, stdout, stderr) => {
              if (err) {
                //some err occurred
                    console.error(err)
                      } else {
                         // the *entire* stdout and stderr (buffered)
                               console.log(`stdout: ${stdout}`);
                               console.log(`stderr: ${stderr}`);
                        }
              });
              let rawdata2 = fs.readFileSync('output.json');
              data2 = JSON.parse(rawdata2);
              console.log(data2);
               
    }
    else {
      console.log("Wrong password.")
    }
    res.render("pages/index", {
      data: data,
      data2: data2
    });
    data.unshift({});
    fs.writeFileSync('data.json', JSON.stringify(data), function (err) {if (err) return err;});

});
