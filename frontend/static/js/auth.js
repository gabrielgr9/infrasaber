document.addEventListener('DOMContentLoaded', () => {
    console.log("InfraSaber: Script de autenticação carregado com sucesso!");

    // ==========================================
    // 0. CONTROLE DE ABAS (Login / Cadastro)
    // ==========================================
    const btnTabLogin = document.getElementById('btn-tab-login');
    const btnTabRegister = document.getElementById('btn-tab-register');
    const formLogin = document.getElementById('form-login');
    const formCadastro = document.getElementById('form-cadastro');

    if (btnTabLogin && btnTabRegister && formLogin && formCadastro) {
        btnTabLogin.addEventListener('click', () => {
            btnTabLogin.classList.add('active');
            btnTabRegister.classList.remove('active');
            formLogin.classList.add('active');
            formCadastro.classList.remove('active');
        });

        btnTabRegister.addEventListener('click', () => {
            btnTabRegister.classList.add('active');
            btnTabLogin.classList.remove('active');
            formCadastro.classList.add('active');
            formLogin.classList.remove('active');
        });
    }

    // ==========================================
    // 1. LÓGICA DE LOGIN COM REDIRECIONAMENTO POR PERFIL
    // ==========================================
    if (formLogin) {
        formLogin.addEventListener('submit', async (event) => {
            event.preventDefault();

            const emailInput = document.getElementById('login-email')?.value;
            const senhaInput = document.getElementById('login-senha')?.value;

            if (!emailInput || !senhaInput) {
                alert('Por favor, preencha o e-mail e a senha.');
                return;
            }

            try {
                const response = await fetch('/usuarios/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: emailInput,
                        senha: senhaInput
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    // Salva os tokens no navegador
                    localStorage.setItem('access_token', data.access_token);
                    localStorage.setItem('token_type', data.token_type || 'Bearer');

                    // Descobre se o usuário logado é Admin ou Morador para redirecionar certo
                    try {
                        const userRes = await fetch('/usuarios/me', {
                            headers: { 'Authorization': `${data.token_type || 'Bearer'} ${data.access_token}` }
                        });

                        if (userRes.ok) {
                            const userData = await userRes.json();
                            const tipoUsuario = userData.tipo ? userData.tipo.toLowerCase() : 'morador';

                            alert('Login realizado com sucesso!');

                            if (tipoUsuario === 'admin') {
                                window.location.href = '/conta';
                            } else {
                                window.location.href = '/conta';
                            }
                            return;
                        }
                    } catch (err) {
                        console.warn("Não foi possível validar o tipo de usuário automaticamente, enviando para o painel de morador.", err);
                    }

                    // Fallback caso falhe a checagem do /me
                    window.location.href = '/login';

                } else {
                    const errorData = await response.json();
                    alert(`Erro ao fazer login: ${errorData.detail || 'E-mail ou senha incorretos'}`);
                }
            } catch (error) {
                console.error('Erro na requisição de login:', error);
                alert('Erro de conexão com o servidor.');
            }
        });
    }

    // ==========================================
    // 2. LÓGICA DE CADASTRO / REGISTRO
    // ==========================================
    if (formCadastro) {
        formCadastro.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log("Botão de cadastrar acionado com sucesso!");

            const nomeInput = document.getElementById('reg-nome')?.value;
            const emailInput = document.getElementById('reg-email')?.value;
            const senhaInput = document.getElementById('reg-senha')?.value;
            const tipoInput = document.getElementById('reg-tipo')?.value || 'morador';

            if (!nomeInput || !emailInput || !senhaInput) {
                alert('Por favor, preencha todos os campos obrigatórios.');
                return;
            }

            try {
                const response = await fetch('/usuarios/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        nome: nomeInput,
                        email: emailInput,
                        senha: senhaInput,
                        tipo: tipoInput.toLowerCase()
                    })
                });

                if (response.ok) {
                    alert('Conta criada com sucesso! Faça login para continuar.');
                    formCadastro.reset();
                    
                    // Muda automaticamente para a aba de login após cadastrar
                    if (btnTabLogin) btnTabLogin.click();
                } else {
                    const errorData = await response.json();
                    let mensagemErro = 'Erro ao cadastrar.';
                    if (Array.isArray(errorData.detail)) {
                        mensagemErro = errorData.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join('\n');
                    } else if (errorData.detail) {
                        mensagemErro = errorData.detail;
                    }
                    alert(mensagemErro);
                }
            } catch (error) {
                console.error('Erro na requisição de cadastro:', error);
                alert('Erro de conexão com o servidor.');
            }
        });
    }
});