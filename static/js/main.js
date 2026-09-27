// =================================
// Auto Close Alerts
// =================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const alerts =
            document.querySelectorAll(
                ".alert"
            );

        alerts.forEach(alert => {

            setTimeout(() => {

                const bsAlert =
                    bootstrap.Alert
                    .getOrCreateInstance(
                        alert
                    );

                bsAlert.close();

            }, 4000);

        });

    }
);


// =================================
// Delete Confirmation
// =================================

function confirmDelete(message){

    return confirm(
        message ||
        "Are you sure?"
    );
}


// =================================
// Date Validation
// =================================

document.addEventListener(
    "DOMContentLoaded",
    function(){

        const start =
            document.getElementById(
                "start_date"
            );

        const end =
            document.getElementById(
                "end_date"
            );

        if(start && end){

            const today =
                new Date()
                .toISOString()
                .split("T")[0];

            start.min = today;

            end.min = today;

            start.addEventListener(
                "change",
                function(){

                    end.min =
                        start.value;

                }
            );

        }

    }
);


// =================================
// Image Preview
// =================================

document.addEventListener(
    "DOMContentLoaded",
    function(){

        const imageInput =
            document.querySelector(
                'input[type="file"]'
            );

        const preview =
            document.getElementById(
                "imagePreview"
            );

        if(imageInput && preview){

            imageInput.addEventListener(
                "change",
                function(){

                    const file =
                        this.files[0];

                    if(file){

                        const reader =
                            new FileReader();

                        reader.onload =
                            function(e){

                            preview.src =
                                e.target.result;

                            preview.style.display =
                                "block";
                        };

                        reader.readAsDataURL(
                            file
                        );

                    }

                }
            );

        }

    }
);