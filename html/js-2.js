document.querySelector(".check_card_info").addEventListener("click", check);

function check() {
    let input_string = document.querySelector("#alphabet_name").value;
    let error_text = "";

    if (input_string.length < 1) {
        error_text = error_text + "名前を入力してください。";
    }

    if (!input_string.match(/^[A-Z]+$/)) {
        error_text = error_text + "\n大文字のアルファベットで入力してください。";
    }

    if (error_text.length > 0) {
        document.querySelector(".error").textContent = error_text;
        document.querySelector("#alphabet_name").style.backgroundColor = "#FADBDA";
    } else {
        document.querySelector(".error").textContent = "";
        document.querySelector("#alphabet_name").style.backgroundColor = "#CEE6C1";
    }
}