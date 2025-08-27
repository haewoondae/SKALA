<template>
  <div class="container-fluid">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card mb-4" v-for="post in posts" :key="post.id">
          <div class="card-header d-flex align-items-center">
            <img :src="post.userAvatar" class="rounded-circle me-2" width="32" height="32">
            <strong>{{ post.username }}</strong>
          </div>
          
          <img :src="post.image" class="card-img-top">
          
          <div class="card-body">
            <div class="d-flex justify-content-between mb-3">
              <div>
                <button class="btn btn-link p-0 me-3" @click="toggleLike(post.id)">
                  <i :class="post.isLiked ? 'bi bi-heart-fill text-danger' : 'bi bi-heart'"></i>
                </button>
                <button class="btn btn-link p-0">
                  <i class="bi bi-chat"></i>
                </button>
              </div>
            </div>
            
            <div class="mb-2">
              <strong>{{ post.likes }} likes</strong>
            </div>
            
            <div class="mb-3">
              <strong>{{ post.username }}</strong>
              {{ post.caption }}
            </div>
            
            <div class="comments mb-3">
              <div v-for="comment in post.comments" :key="comment.id" class="mb-1">
                <strong>{{ comment.username }}</strong> {{ comment.text }}
              </div>
            </div>
            
            <div class="input-group">
              <input 
                type="text" 
                class="form-control border-0" 
                placeholder="Add a comment..."
                v-model="newComments[post.id]"
                @keyup.enter="addComment(post.id)"
              >
              <button 
                class="btn btn-link" 
                type="button"
                @click="addComment(post.id)"
              >
                Post
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <nav class="navbar fixed-bottom navbar-light bg-white border-top">
      <div class="container-fluid justify-content-around">
        <button class="btn btn-link">
          <i class="bi bi-house fs-4"></i>
        </button>
        <button class="btn btn-link">
          <i class="bi bi-search fs-4"></i>
        </button>
        <button class="btn btn-link">
          <i class="bi bi-plus-square fs-4"></i>
        </button>
        <button class="btn btn-link">
          <i class="bi bi-heart fs-4"></i>
        </button>
        <button class="btn btn-link">
          <i class="bi bi-person-circle fs-4"></i>
        </button>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const posts = ref([
  {
    id: 1,
    username: 'user1',
    userAvatar: 'https://via.placeholder.com/32',
    image: 'https://via.placeholder.com/400x300',
    caption: 'Beautiful sunset!',
    likes: 42,
    isLiked: false,
    comments: [
      { id: 1, username: 'friend1', text: 'Amazing!' },
      { id: 2, username: 'friend2', text: 'Love this!' }
    ]
  },
  {
    id: 2,
    username: 'user2',
    userAvatar: 'https://via.placeholder.com/32',
    image: 'https://via.placeholder.com/400x300',
    caption: 'Good morning!',
    likes: 28,
    isLiked: true,
    comments: [
      { id: 3, username: 'friend3', text: 'Good morning!' }
    ]
  }
])

const newComments = reactive({})

const toggleLike = (postId) => {
  // 좋아요 토글 로직
}

const addComment = (postId) => {
  // 댓글 추가 로직
}
</script>
