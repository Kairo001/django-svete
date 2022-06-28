
<script>
    import axios from 'axios'
    import {push} from 'svelte-spa-router'
    let first_name = '', last_name = '', email = '', password = '', password_confirm = ''

    $: submit = async () => {
        await axios.post('register/', {
            first_name,
            last_name,
            email,
            password,
            password_confirm
        })

        await push('/login')
    }
</script>

<main class="form-signin">
	<form on:submit|preventDefault={submit}>
		<h1 class="h3 mb-3 fw-normal text-center">Por favor regístrate</h1>

        <div class="form-floating">
            <input bind:value={first_name} class="form-control" id="id_first_name" placeholder="Nombre">
            <label for="id_first_name">Nombre</label>
        </div>
	
		<div class="form-floating">
		  <input bind:value={last_name} class="form-control" id="id_last_name" placeholder="Apellido">
		  <label for="id_last_name">Apellido</label>
		</div>

        <div class="form-floating">
            <input bind:value={email} type="email" class="form-control" id="id_email" placeholder="name@example.com">
            <label for="id_email">Correo electrónico</label>
        </div>

		<div class="form-floating">
		  <input bind:value={password} type="password" class="form-control" id="id_password" placeholder="Password">
		  <label for="id_password">Contraseña</label>
		</div>

        <div class="form-floating">
            <input bind:value={password_confirm} type="password" class="form-control" id="id_password_confirm" placeholder="Password">
            <label for="id_password_confirm">Confirmar contraseña</label>
        </div>

		<button class="w-100 btn btn-lg btn-primary" type="submit">Registrar</button>
	</form>
</main>
