<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Sign Up</h3>
            <form>
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="name" 
                  v-model="name"
                  placeholder="Enter your name" 
                />
              </div>
              
              <div class="mb-3">
                <label for="email" class="form-label">Email (ID)</label>
                <div class="input-group">
                  <input 
                    type="email" 
                    class="form-control" 
                    id="email" 
                    v-model="email"
                    placeholder="Enter your email" 
                  />
                  <button 
                    class="btn btn-outline-primary" 
                    type="button"
                    @click="checkEmailDuplicate"
                  >
                    Check
                  </button>
                </div>
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password" 
                  v-model="password"
                  placeholder="Enter password" 
                />
              </div>
              
              <div class="mb-3">
                <label for="passwordConfirm" class="form-label">Confirm Password</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="passwordConfirm" 
                  v-model="passwordConfirm"
                  placeholder="Confirm password" 
                />
              </div>
              
              <div class="d-grid gap-2">
                <button 
                  type="button" 
                  class="btn btn-primary"
                  @click="handleSignUp"
                >
                  Sign Up
                </button>
                <button 
                  type="button" 
                  class="btn btn-outline-secondary"
                  @click="goToLogin"
                >
                  Go to Login
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


const name = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')

const checkEmailDuplicate = () => {
  // 이메일 중복 확인 로직
}

const handleSignUp = () => {
  // 회원가입 로직
}

const goToLogin = () => {
  // 로그인 화면으로 이동
  router.push('/login')
}
</script>
