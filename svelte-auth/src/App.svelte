<script>
	import Home from "./pages/Home.svelte"
	import Login from "./pages/Login.svelte"
	import Register from "./pages/Register.svelte"

	import Router, {link} from 'svelte-spa-router'
  import axios from "axios";
  import { authenticated } from "./store/auth";

	const routes = {
		'/': Home,
		'/login': Login,
		'/register': Register
	}

  let auth = false

  authenticated.subscribe(value => auth = value)

  $: logout = async () => {
    await axios.post('logout/', {}, {withCredentials:true})

    axios.defaults.headers.common['Authorization'] = ''

    authenticated.set(false)
  }

</script>

<header class="p-3 bg-dark text-white">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li><a href="/" use:link class="nav-link px-2 text-white">About</a></li>
        </ul>

        <!-- <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3">
          <input type="search" class="form-control form-control-dark" placeholder="Search..." aria-label="Search">
        </form> -->

        {#if auth}
          <div class="text-end">
            <a href="/login" use:link class="btn btn-outline-light me-2"
              on:click={logout}
            >Cerrar sesión</a>
          </div>
        {:else}
          <div class="text-end">
            <a href="/login" use:link class="btn btn-outline-light me-2">Iniciar sesión</a>
            <a href="/register" use:link class="btn btn-outline-light me-2">Registarse</a>
          </div>
        {/if}
      </div>
    </div>
</header>

<Router routes={routes} />

