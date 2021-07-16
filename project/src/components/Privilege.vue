<template>
	<main>
		<div class="wrap">
			<nav aria-label="breadcrumb" class="wrap-in">
				<ol class="breadcrumb">
					<li class="breadcrumb-item"><router-link to="/userPage">Главная</router-link></li>
					<li class="breadcrumb-item">Программа привилегий</li>
				</ol>
			</nav>
		</div>

		<div class="wrap text">
			<div class="wrap-in">
				<h1>Программа привилегий</h1>
			</div>
		</div>
	</main>
</template>

<style scoped>

main{
	width: 100%;
    height: 100%;
}

.wrap{
	width: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
}

.wrap-in{
	width: 80%;;
}

nav{
	margin-top: 50px;
}
h1{
	font-size: 3em;
	font-weight: bold;
	text-align: left;
}

a{
	text-decoration: none !important;
}
</style>