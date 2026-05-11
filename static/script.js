const input = document.getElementById("lineInput");
const counter = document.getElementById("counter");

if(input){

    input.addEventListener("input", () => {

        counter.textContent =
        `${input.value.length} / 180`;

    });

}