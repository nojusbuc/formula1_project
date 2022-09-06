// var python_process;

// router.get('/start_python', function (req, res) {
//     const { PythonShell } = require("python-shell");

//     var options = {
//         pythonPath: 'local python path'
//     }
//     var pyshell = new PythonShell('general.py');

//     pyshell.end(function (err) {
//         if (err) {
//             console.log(err);
//         }
//     });
//     python_process = pyshell.childProcess;

//     res.send('Started.');
// });

// router.get('/stop_python', function (req, res) {
//     python_process.kill('SIGINT');
//     res.send('Stopped');
// });