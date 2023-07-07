const radioInputs = document.getElementsByName("flexRadioQB");
const submitButton = document.getElementById("img");

radioInputs.forEach(function(radioInput) {
  radioInput.addEventListener("change", function() {
    if (this.checked) {
      submitButton.value = this.value;
    }
  });
});