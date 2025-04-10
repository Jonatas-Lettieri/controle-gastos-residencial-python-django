// Utilizei javascript para colocar aquele aviso de navegador no projeto

document.addEventListener("DOMContentLoaded", function() {
    // Acessa o elemento select[name='tipo'] de forma mais segura possível
    const tipoTransacao = document.querySelector("select[name='tipo']");
    
    // Verifica se o elemento foi encontrado antes de adicionar o evento
    if (tipoTransacao) {
        tipoTransacao.addEventListener("change", function() {
            // Verifica se o valor selecionado é "receita"
            if (this.value === "receita") {
                // Exibe um alerta
                alert("Apenas usuários com mais de 18 anos podem realizar transações de receita.");
            }
        });
    } else {
        // Caso o elemento não seja encontrado, exibe uma mensagem de erro no console
        console.log("Elemento select[name='tipo'] não encontrado!");
    }
});
