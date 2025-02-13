<script lang="ts">
    export let favorites: {username: string; content: string}[];
</script>

<div class="box">
    <h3>Favorites</h3>
    <ul class="favorite-list">
        {#each favorites as fav}
            <li class="favorite-item box">
                <strong>{fav.username}</strong>: {fav.content}
            </li>
        {/each}
    </ul>
</div>

<style>
    .favoretes-list {
        list-style-type: none;
        padding: 0;
    }
    
    .favorite-item {
        margin-bottom: 10px;
    }
</style>