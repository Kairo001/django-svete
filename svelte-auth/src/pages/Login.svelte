
<script>
    import axios from 'axios'
    import {push} from 'svelte-spa-router'
    import { authenticated } from '../store/auth';
    let email = '', password = ''

    $: submit = async () => {
        const {data} = await axios.post('login/', {
            email,
            password
        }, {withCredentials: true})

		axios.defaults.headers.common['Authorization'] = `Bearer ${data.token}`
        document.cookie = `refresh_token=${data.refresh_token}`
        authenticated.set(true)
        await push('/')
    }
</script>

<main class="form-signin">
	<form on:submit|preventDefault={submit}>
		<h1 class="h3 mb-3 fw-normal text-center">Por favor inicia sesión</h1>

        <div class="form-floating">
            <input bind:value={email} type="email" class="form-control" id="id_email" placeholder="name@example.com">
            <label for="id_email">Correo electrónico</label>
        </div>

		<div class="form-floating">
		  <input bind:value={password} type="password" class="form-control" id="id_password" placeholder="Password">
		  <label for="id_password">Contraseña</label>
		</div>

		<button class="w-100 btn btn-lg btn-primary" type="submit">Iniciar sesión</button>
	</form>
</main>

