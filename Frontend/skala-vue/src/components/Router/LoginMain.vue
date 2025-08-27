<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Login</h3>
            <form>
              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="email" 
                  v-model="email"
                  placeholder="Enter email" 
                />
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <div class="input-group">
                  <input 
                    :type="showPassword ? 'text' : 'password'" 
                    class="form-control" 
                    id="password"
                    v-model="password"
                    placeholder="Enter password" 
                  />
                  <button 
                    class="btn btn-outline-secondary" 
                    type="button"
                    @click="togglePassword"
                  >
                    <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                  </button>
                </div>
              </div>
              
              <div class="d-grid gap-2">
                <button 
                  type="button" 
                  class="btn btn-primary"
                  @click="handleLogin"
                >
                  Login
                </button>
                <button 
                  type="button" 
                  class="btn btn-outline-secondary"
                  @click="handleSignUp"
                >
                  Sign Up
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

function gotoSignup() {
  router.push('/signup')
}

const email = ref('')
const password = ref('')
const showPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const handleLogin = () => {
  // 로그인 로직
}

const handleSignUp = () => {
  // 회원가입 로직
    gotoSignup()
}


</script>
