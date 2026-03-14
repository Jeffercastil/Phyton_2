/**
 * Validación del formulario de registro
 * Proporciona retroalimentación en tiempo real al usuario
 */

(function() {
    'use strict';

    // Esperar a que el DOM esté listo
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('registerForm');
        const passwordInput = document.getElementById('password');
        const passwordConfirmInput = document.getElementById('password_confirm');
        const reqLength = document.getElementById('req-length');
        const reqMatch = document.getElementById('req-match');
        const submitBtn = document.getElementById('submitBtn');

        // Si no estamos en la página de registro, salir
        if (!form) return;

        /**
         * Validar longitud de contraseña
         */
        function validateLength() {
            const isValid = passwordInput.value.length >= 6;
            updateRequirement(reqLength, isValid);
            return isValid;
        }

        /**
         * Validar que las contraseñas coincidan
         */
        function validateMatch() {
            const password = passwordInput.value;
            const confirm = passwordConfirmInput.value;
            const isValid = password === confirm && password !== '';
            updateRequirement(reqMatch, isValid);
            return isValid;
        }

        /**
         * Actualizar el estado visual de un requisito
         */
        function updateRequirement(element, isValid) {
            if (!element) return;

            const icon = element.querySelector('i');

            if (isValid) {
                element.classList.add('valid');
                if (icon) {
                    icon.className = 'fas fa-check-circle';
                    icon.style.color = '#10b981';
                }
            } else {
                element.classList.remove('valid');
                if (icon) {
                    icon.className = 'fas fa-circle';
                    icon.style.color = '#9ca3af';
                }
            }
        }

        /**
         * Validar todo el formulario
         */
        function validateForm() {
            const isLengthValid = validateLength();
            const isMatchValid = validateMatch();

            // Habilitar/deshabilitar botón basado en validación
            if (isLengthValid && isMatchValid && passwordInput.value !== '') {
                submitBtn.style.opacity = '1';
                submitBtn.style.cursor = 'pointer';
                submitBtn.disabled = false;
            } else {
                submitBtn.style.opacity = '0.7';
                submitBtn.style.cursor = 'not-allowed';
                submitBtn.disabled = true;
            }

            return isLengthValid && isMatchValid;
        }

        // Event listeners para validación en tiempo real
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                validateLength();
                validateMatch();
                validateForm();
            });

            passwordInput.addEventListener('blur', validateLength);
        }

        if (passwordConfirmInput) {
            passwordConfirmInput.addEventListener('input', function() {
                validateMatch();
                validateForm();
            });

            passwordConfirmInput.addEventListener('blur', validateMatch);
        }

        // Validación final antes de enviar
        if (form) {
            form.addEventListener('submit', function(event) {
                if (!validateForm()) {
                    event.preventDefault();

                    // Mostrar mensaje de error
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'alert-msg alert-error';
                    errorDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> Por favor, verifica que la contraseña cumpla con todos los requisitos.';

                    // Insertar al inicio del formulario
                    const firstChild = form.firstChild;
                    form.insertBefore(errorDiv, firstChild);

                    // Remover después de 5 segundos
                    setTimeout(() => {
                        if (errorDiv.parentNode) {
                            errorDiv.parentNode.removeChild(errorDiv);
                        }
                    }, 5000);

                    return false;
                }

                // Mostrar estado de carga
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creando cuenta...';
                submitBtn.disabled = true;
            });
        }

        // Validación inicial
        validateForm();

        // Animación de entrada para la tarjeta
        const registerCard = document.querySelector('.register-card');
        if (registerCard) {
            registerCard.style.opacity = '0';
            registerCard.style.transform = 'translateY(20px)';

            setTimeout(() => {
                registerCard.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                registerCard.style.opacity = '1';
                registerCard.style.transform = 'translateY(0)';
            }, 100);
        }

        // Auto-formatear teléfono
        const telefonoInput = document.getElementById('telefono');
        if (telefonoInput) {
            telefonoInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 10) {
                    value = value.substring(0, 10);
                }
                e.target.value = value;
            });
        }
    });
})();
