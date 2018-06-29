function initCanvas(current_image_url, boxes) {
    const canvas = $('#canvas')[0];
    const ctx = canvas.getContext('2d');

    function drawBoxes(boxes, storkeColor) {
        ctx.strokeStyle = storkeColor;
        ctx.fillStyle = storkeColor;
        ctx.lineWidth = 4;

        boxes.forEach((box) => {
            ctx.beginPath();
            ctx.rect(box[0], box[1], box[2] - box[0], box[3] - box[1]);
            ctx.stroke();

            ctx.save();
            ctx.font = "15px Arial";
            const text = box[5].toFixed(2).toString();
            const width = ctx.measureText(text).width;

            ctx.textBaseline = 'top';
            ctx.fillStyle = storkeColor;
            ctx.fillRect(box[0]-2, box[1] - 19, width+8, 19);

            ctx.fillStyle = 'white';
            ctx.fillText(text, box[0]+2, box[1]-16);

            ctx.restore();
        });
    }

    function update_image() {
        let states = [
            $('#cb-boxes1').prop('checked'),
            $('#cb-boxes2').prop('checked')
        ];

        ctx.drawImage(image, 0, 0);
        if (states[0]) {
            drawBoxes(boxes.boxes1, 'red');
        }
        if (states[1]) {
            drawBoxes(boxes.boxes2, 'blue');
        }
    }


    let image = new Image();
    image.display = 'block';

    image.onload = () => {
        canvas.width = image.width;
        canvas.height = image.height;

        update_image();
    };
    image.src = current_image_url;

    $('#cb-boxes1, #cb-boxes2').click((e) => {
        update_image();
    });
}