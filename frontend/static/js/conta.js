document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem("access_token");
    const tokenType = localStorage.getItem("token_type") || "Bearer";

    if (!token) {
        window.location.href = "/login";
        return;
    }

    const elNome = document.getElementById('usuario-nome');
    const elEmail = document.getElementById('usuario-email');
    const elTipo = document.getElementById('usuario-tipo');

    let usuarioAtual = null;

    try {
        const response = await fetch('/usuarios/me', {
            headers: { 'Authorization': `${tokenType} ${token}` }
        });

        if (response.ok) {
            usuarioAtual = await response.json();
            if (elNome) elNome.textContent = usuarioAtual.nome || '-';
            if (elEmail) elEmail.textContent = usuarioAtual.email || '-';
            if (elTipo) elTipo.textContent = (usuarioAtual.tipo || '-').toUpperCase();
        } else if (response.status === 401) {
            localStorage.clear();
            window.location.href = "/login";
        }
    } catch (error) {
        console.error("Erro ao carregar dados da conta:", error);
    }

    // Logout
    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) {
        btnLogout.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.clear();
            alert('Sessão encerrada com sucesso.');
            window.location.href = "/login";
        });
    }

    // Alterar senha
    const formSenha = document.getElementById('formAlterarSenha');
    const mensagemAlerta = document.getElementById('mensagemAlerta');

    if (formSenha) {
        formSenha.addEventListener('submit', async (e) => {
            e.preventDefault();

            const senhaAtual = document.getElementById('inputSenhaAtual').value;
            const novaSenha = document.getElementById('inputNovaSenha').value;
            const confirmaSenha = document.getElementById('inputConfirmaSenha').value;

            if (novaSenha !== confirmaSenha) {
                mensagemAlerta.innerHTML = `<div class="alert alert-danger">A nova senha e a confirmação não coincidem.</div>`;
                return;
            }
            if (!usuarioAtual) {
                mensagemAlerta.innerHTML = `<div class="alert alert-danger">Não foi possível identificar o usuário logado.</div>`;
                return;
            }

            try {
                // 1. Valida a senha atual reaproveitando o próprio endpoint de login
                const loginCheck = new URLSearchParams();
                loginCheck.append('username', usuarioAtual.email);
                loginCheck.append('password', senhaAtual);

                const respCheck = await fetch('/usuarios/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: loginCheck
                });

                if (!respCheck.ok) {
                    mensagemAlerta.innerHTML = `<div class="alert alert-danger">Senha atual incorreta.</div>`;
                    return;
                }

                // 2. Atualiza, mandando nome/email/tipo intactos + a nova senha
                const respUpdate = await fetch(`/usuarios/${usuarioAtual.id_usuario}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `${tokenType} ${token}`
                    },
                    body: JSON.stringify({
                        nome: usuarioAtual.nome,
                        email: usuarioAtual.email,
                        senha: novaSenha,
                        tipo: usuarioAtual.tipo
                    })
                });

                if (respUpdate.ok) {
                    mensagemAlerta.innerHTML = `<div class="alert alert-success">Senha atualizada com sucesso!</div>`;
                    formSenha.reset();
                } else {
                    const err = await respUpdate.json();
                    mensagemAlerta.innerHTML = `<div class="alert alert-danger">Erro ao atualizar: ${err.detail || 'Erro desconhecido'}</div>`;
                }
            } catch (error) {
                console.error("Erro ao alterar senha:", error);
                mensagemAlerta.innerHTML = `<div class="alert alert-danger">Erro de conexão ao alterar a senha.</div>`;
            }
        });
    }
});