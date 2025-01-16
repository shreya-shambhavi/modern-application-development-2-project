<template>
    <div class="unauthorized">
        <div>
            <h1>Unauthorized</h1>
            <p>You do not have permission to access this page.</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'UnauthorizedView',
};
</script>

<style scoped>
.unauthorized {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 250px;
    text-align: center;
}
h1 {
    font-size: 6em;
    margin-bottom: 20px;
}
p {
    font-size: 1em;
}
</style>
