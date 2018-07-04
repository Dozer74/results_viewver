function initCanvas(current_image_url, boxes) {
    const canvas = $('#canvas')[0];
    const ctx = canvas.getContext('2d');
    const slider = $("#slider");

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
            ctx.fillRect(box[0] - 2, box[1] - 19, width + 8, 19);

            ctx.fillStyle = 'white';
            ctx.fillText(text, box[0] + 2, box[1] - 16);

            ctx.restore();
        });
    }

    function getCheckboxStates() {
        const cbBoxes = $('.cb-boxes');
        return cbBoxes.map((i, el) => $(el).prop('checked')).get();
    }

    function loadStates() {
        let states = sessionStorage.getItem('states');
        if (states) {
            states = JSON.parse(states);
            let checkBoxes = $('.cb-boxes');
            if (states.length === checkBoxes.length) {
                checkBoxes.each((idx, el) => $(el).prop('checked', states[idx]));
            }
        }

        let threshold = sessionStorage.getItem('threshold');
        if (threshold) {
            threshold = Number.parseFloat(threshold);
            slider.slider('setValue', threshold);
            $("#slider-value").text(threshold);
        }
    }

    function update_image() {
        ctx.drawImage(image, 0, 0);

        let states = getCheckboxStates();
        let threshold = Number.parseFloat(slider.val());
        for (let i = 0; i < states.length; i++) {
            if (states[i]) {
                const selected_boxes = boxes[i].boxes.filter(box => box[5] >= threshold);
                drawBoxes(selected_boxes, boxes[i].color);
            }
        }
    }


    let image = new Image();
    image.display = 'block';

    image.onload = () => {
        canvas.width = image.width;
        canvas.height = image.height;

        loadStates();
        update_image();
    };
    image.src = current_image_url;


    $('.cb-boxes').click((e) => {
        update_image();

        const states = getCheckboxStates();
        sessionStorage.setItem('states', JSON.stringify(states));
    });

    $(document).ready($ => {
        slider.slider();

        const update = (newValue) => {
            $("#slider-value").text(newValue);
            update_image();
            sessionStorage.setItem('threshold', JSON.stringify(newValue));
        };

        slider.on('change', (e) => update(e.value.newValue));
        slider.on("slide", (e) => update(e.value));
    });


}