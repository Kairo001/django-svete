<script>
    import {onMount} from 'svelte'
    import axios from 'axios'
    import { authenticated } from '../store/auth';
    
    let message = 'No has iniciado sesión.'

    onMount(async () => {
        const {data, status} = await axios.get('user/')
        if (status === 200) {
            message = `Hi ${data.first_name} ${data.last_name}`
            authenticated.set(true)
        } else {
            message = 'No has iniciado sesión.'
            authenticated.set(false)
        }
    })
</script>

<div class="container mt-5 text-center">
    <h3>
        {message}
    </h3>
</div>