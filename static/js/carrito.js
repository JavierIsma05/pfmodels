/*var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'User'){
			addCookieItem(productId, action)
		}
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}
*/
//APLICANDO EL PATRÓN MEMENTO
// Paso 1: Identificar el estado relevante
var cartState = {
    items: [], // Lista de elementos en el carrito
    totalPrice: 0 // Precio total del carrito
};

// Paso 2: Crear la clase Memento
class CartMemento {
    constructor(state) {
        this.state = state;
    }

    getState() {
        return this.state;
    }
}

// Crear una variable para almacenar el último estado del carrito
var lastCartState = null;

// Función para guardar el estado del carrito como Memento
function saveCartState() {
    lastCartState = new CartMemento(Object.assign({}, cartState));
}

// Función para restaurar el estado del carrito desde un Memento
function restoreCartState() {
    if (lastCartState !== null) {
        cartState = Object.assign({}, lastCartState.getState());
    }
}

// Modificar el código existente para manejar el Memento
var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);

        // Guardar el estado actual del carrito antes de realizar la actualización
        saveCartState();

        console.log('USER:', user);

        if (user === 'User') {
            addCookieItem(productId, action);
        }
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }

        // Restaurar el estado del carrito si es necesario
        restoreCartState();
    });
}

function updateUserOrder(productId, action){
	console.log('Ususario autenticado, enviando data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}


function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('eliminar-todo').addEventListener('click', function() {
        if (confirm('¿Estás seguro de que deseas eliminar todos los productos?')) {
            eliminarTodosLosProductos();
        }
    });

    function eliminarTodosLosProductos() {
        var productos = document.querySelectorAll('.product');
        productos.forEach(function(producto) {
            producto.parentNode.removeChild(producto);
        });

        // Vaciar el carrito
        cart = {};

        // Actualizar la cookie del carrito
        document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";

        // Si el usuario está logeado, también podrías enviar una solicitud al servidor
        // para actualizar la información del carrito en la base de datos
        if (usuarioLogeado) {
            actualizarCarritoEnServidor(cart);
        }

        // Recargar la página o actualizar la interfaz según sea necesario
        location.reload();
    }

    // Función para actualizar el carrito en el servidor (solo si el usuario está logeado)
    function actualizarCarritoEnServidor(cart) {
		// Convertir el objeto cart a formato JSON
		var jsonData = JSON.stringify(cart);
	
		// Configurar la solicitud HTTP
		fetch('/actualizar-carrito', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: jsonData
		})
		.then(response => {
			if (!response.ok) {
				throw new Error('La solicitud de actualización del carrito falló');
			}
			// Opcional: procesar la respuesta del servidor
			return response.json();
		})
		.then(data => {
			// Opcional: manejar la respuesta del servidor
			console.log('Carrito actualizado correctamente:', data);
		})
		.catch(error => {
			console.error('Error al actualizar el carrito:', error);
		});
	}	
});

