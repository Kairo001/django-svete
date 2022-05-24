<script>
	import Home from "./pages/Home.svelte"
	import Login from "./pages/Login.svelte"
	import Register from "./pages/Register.svelte"

	import Router, {link} from 'svelte-spa-router'

	const routes = {
		'/': Home,
		'/login': Login,
		'/register': Register
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

        <div class="text-end">
          <a href="/login" use:link type="button" class="btn btn-outline-light me-2">Iniciar sesión</a>
          <a href="/register" use:link type="button" class="btn btn-outline-light me-2">Registarse</a>
        </div>
      </div>
    </div>
</header>

<Router routes={routes} />

