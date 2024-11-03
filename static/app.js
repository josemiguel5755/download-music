// document.getElementById('downloadForm').addEventListener('submit', async function(e) {
//     e.preventDefault();

//     const url = document.getElementById('url').value;
//     const status = document.getElementById('status');

//     status.textContent = 'Descargando...';

//     try {
//         const response = await fetch('/download', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ url: url }),
//         });

//         if (response.ok) {
//             const contentType = response.headers.get('Content-Type');

//             if (contentType === 'application/json') {
//                 // Manejo del caso de error JSON
//                 const errorData = await response.json();
//                 status.textContent = errorData.error || 'Error downloading the video.';
//             } else {
//                 // Manejo de la descarga del archivo
//                 const blob = await response.blob();
//                 const downloadUrl = window.URL.createObjectURL(blob);
//                 const a = document.createElement('a');
//                 a.href = downloadUrl;
//                 a.download = 'audio.mp3';
//                 document.body.appendChild(a);
//                 a.click();
//                 a.remove();
//                 status.textContent = 'Descarga completa!';
//             }
//         } else {
//             status.textContent = 'Error de Descarga.';
//         }
//     } catch (error) {
//         status.textContent = 'Se produjo un error: ' + error.message;
//     }
// });


document.getElementById('downloadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const url = document.getElementById('url').value;
    const status = document.getElementById('status');
    status.textContent = 'Iniciando descarga...';

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        if (response.ok) {
            const contentType = response.headers.get('Content-Type');

            if (contentType === 'application/json') {
                const errorData = await response.json();
                status.textContent = errorData.error || 'Error downloading the video.';
            } else {
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = 'audio.mp3';
                document.body.appendChild(a);
                a.click();
                a.remove();
                status.textContent = 'Descarga completa!';
            }
        } else {
            status.textContent = 'Error de Descarga.';
        }
    } catch (error) {
        status.textContent = 'Se produjo un error: ' + error.message;
    }
});

// WebSocket para actualizar el progreso en tiempo real
const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

socket.on('download_progress', function(data) {
    const status = document.getElementById('status');
    status.textContent = `Descargando... ${data.progress}`;
});
