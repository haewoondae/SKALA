<template>
  <div class="container-sm mt-3 border border-2 p-1" style="max-width: 600px">                     <!-- 최대 600px 너비의 작은 컨테이너, 상단 여백, 테두리, 패딩 적용 -->
    <div class="bss-background p-1">                                                                <!-- 배경 이미지가 적용된 컨테이너 -->
      <div class="mt-3 d-flex justify-content-center" style="height: 230px;">                      <!-- 높이 230px의 중앙 정렬 컨테이너 -->
        <span class="text-center text-danger fs-1 fw-bold mt-4">SKALA STOCK Market</span>          <!-- 빨간색, 큰 글씨, 굵은 글꼴의 제목 -->
      </div>
      <div class="row bg-info-subtle p-2 m-1" style="opacity: 95%;">                               <!-- 연한 파란색 배경, 95% 투명도의 로그인 폼 영역 -->
        <div class="col">                                                                           <!-- 입력 필드를 담는 컬럼 -->
          <InlineInput v-model="playerId" label="플레이어ID" class="mb-1" type="text" placeholder="플레이어ID" />              <!-- 플레이어 ID 입력 필드 (양방향 바인딩) -->
          <InlineInput v-model="playerPassword" label="비밀번호" class="mb-1" type="password" placeholder="비밀번호" />        <!-- 비밀번호 입력 필드 (마스킹 처리) -->
        </div>
        <div class="d-flex justify-content-end" >                                                   <!-- 버튼을 오른쪽 정렬하는 컨테이너 -->
          <button v-if = "isNewPlayer" @click="signup" class="btn btn-primary btn-sm" >회원가입</button>                      <!-- 신규 사용자일 때 회원가입 버튼 표시 -->
          <button v-else @click="login" class="btn btn-primary btn-sm">로그인</button>                                        <!-- 기존 사용자일 때 로그인 버튼 표시 -->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';                                                               // Vue 3의 반응형 데이터 생성 함수들 임포트
import { useRouter } from 'vue-router';                                                            // Vue Router의 라우팅 기능 사용을 위한 훅 임포트
import apiCall from '@/scripts/api-call';                                                          // 커스텀 API 호출 유틸리티 임포트
import { storePlayer } from '@/scripts/store-player';                                              // 플레이어 정보 저장 함수 임포트
import { notifyInfo } from '@/scripts/store-popups';                                               // 알림 팝업 표시 함수 임포트

const router = useRouter();                                                                        // 라우터 인스턴스 생성 (페이지 이동용)

const playerId = ref('');                                                                          // 플레이어 ID 입력값을 저장하는 반응형 변수
const playerPassword = ref('');                                                                    // 비밀번호 입력값을 저장하는 반응형 변수
const playerMoney = ref('');                                                                       // 플레이어 초기 자금 (현재 미사용 - 삭제 가능)
const isNewPlayer = ref(false);                                                                    // 신규 사용자 여부를 나타내는 반응형 변수 (기본값: 기존 사용자)

// ===================================================================================================
// GPT 버전 로그인 함수 (주석 처리된 고급 버전 - 에러 처리 포함)
// ===================================================================================================
// const login = async () => {                                                                      // 비동기 로그인 함수 정의
//   // 로그인 로직 작성 (POST /api/players/login 호출)
//   try {                                                                                          // 에러 처리를 위한 try-catch 블록 시작
//     const url = '/api/players/login';                                                            // API 엔드포인트 URL 정의
//     const requestBody = {                                                                        // 서버에 전송할 요청 데이터 객체
//       playerId: playerId.value,                                                                  // 입력받은 플레이어 ID (.value로 ref 값 접근)
//       playerPassword: playerPassword.value                                                       // 입력받은 비밀번호 (.value로 ref 값 접근)
//     };
    
//     const response = await apiCall.post(url, null, requestBody);                                 // POST 요청으로 로그인 시도 (응답 대기)
    
//     if (response.result === apiCall.Response.SUCCESS) {                                          // 로그인 성공 여부 확인
//       // 로그인 성공시 플레이어 정보 저장
//       storePlayer(response.body);                                                                // 응답받은 플레이어 정보를 로컬 저장소에 저장
//       // stock 페이지로 이동
//       router.push('stock');                                                                      // 주식 거래 페이지로 라우팅
//     } else {                                                                                     // 로그인 실패시
//       // 로그인 실패시 알림
//       notifyInfo(response.message || '로그인에 실패했습니다.');                                     // 에러 메시지 팝업 표시
//     }
//   } catch (error) {                                                                             // 네트워크 오류 등 예외 상황 처리
//     console.error('Login error:', error);                                                       // 콘솔에 에러 로그 출력
//     notifyInfo('로그인 중 오류가 발생했습니다.');                                                    // 사용자에게 에러 알림
//   }
// }   

// ===================================================================================================
// 교수님 버전 로그인 함수 (현재 사용 중인 단순 버전)
// ===================================================================================================
async function login() {                                                                          // 비동기 로그인 함수 정의 (function 선언문 방식)
  if (playerId.value.trim() === '' || playerPassword.value === '') {                                   // 입력값 검증
    notifyInfo('아이디와 비밀번호를 입력하세요.');                                               // 알림 메시지 표시
    return;                                                                                       // 함수 종료
  }

  const url = "/api/players/login";                                                               // API 엔드포인트 URL 정의
  const requestBody = {                                                                           // 서버에 전송할 요청 데이터 객체
    playerId: playerId.value,                                                                     // 입력받은 플레이어 ID (.value로 ref 값 접근)
    playerPassword: playerPassword.value                                                          // 입력받은 비밀번호 (.value로 ref 값 접근)
  };
  const response = await apiCall.post(url, null, requestBody);                                    // POST 요청으로 로그인 시도 (응답 대기)

  if(response.result === 0 ) {                                                                    // 응답 결과가 성공(0)인지 확인
    storePlayer(response.body);                                                                   // 응답받은 플레이어 정보를 로컬 저장소에 저장
    router.push('/stock');                                                                        // 주식 거래 페이지로 라우팅 (절대 경로 사용)

  } else {                                                                                        // 로그인 실패시 (플레이어가 존재하지 않는 경우)
    isNewPlayer.value = true;                                                                     // 신규 사용자 플래그를 true로 설정 (회원가입 버튼 표시)

  }

  console.log(response);                                                                          // 응답 내용을 콘솔에 출력 (디버깅용)
}; 

// ===================================================================================================
// GPT 버전 회원가입 함수 (주석 처리된 고급 버전 - 에러 처리 및 자동 로그인 포함)
// ===================================================================================================
// const signup = async () => {                                                                     // 비동기 회원가입 함수 정의
//   // 회원가입 로직 작성 (POST /api/players 호출)
//   try {                                                                                          // 에러 처리를 위한 try-catch 블록 시작
//     const url = '/api/players';                                                                  // API 엔드포인트 URL 정의
//     const requestBody = {                                                                        // 서버에 전송할 요청 데이터 객체
//       id: 0,                                                                                     // 플레이어 ID (서버에서 자동 생성)
//       playerId: playerId.value,                                                                  // 입력받은 플레이어 ID (.value로 ref 값 접근)
//       playerPassword: playerPassword.value,                                                      // 입력받은 비밀번호 (.value로 ref 값 접근)
//       playerMoney: playerMoney.value || 50000                                                    // 기본 시드머니 설정 (입력값 없으면 50000)
//     };
    
//     const response = await apiCall.post(url, null, requestBody);                                 // POST 요청으로 회원가입 시도 (응답 대기)
    
//     if (response.result === apiCall.Response.SUCCESS) {                                          // 회원가입 성공 여부 확인
//       // 회원가입 성공시 자동 로그인 처리
//       isNewPlayer.value = false;                                                                 // 신규 사용자 플래그를 false로 변경
//       notifyInfo('회원가입이 완료되었습니다.');                                                      // 성공 메시지 팝업 표시
//       // 로그인 함수 호출
//       await login();                                                                             // 회원가입 후 자동으로 로그인 시도
//     } else {                                                                                     // 회원가입 실패시
//       // 회원가입 실패시 알림
//       notifyInfo(response.message || '회원가입에 실패했습니다.');                                    // 에러 메시지 팝업 표시
//     }
//   } catch (error) {                                                                             // 네트워크 오류 등 예외 상황 처리
//     console.error('Signup error:', error);                                                      // 콘솔에 에러 로그 출력
//     notifyInfo('회원가입 중 오류가 발생했습니다.');                                                   // 사용자에게 에러 알림
//   }
// }

// ===================================================================================================
// 교수님 버전 회원가입 함수 (현재 사용 중인 단순 버전)
// ===================================================================================================
const signup = async () => {                                                                      // 비동기 회원가입 함수 정의 (화살표 함수 방식)
  const url = "/api/players"                                                                      // API 엔드포인트 URL 정의
  const requestBody = {                                                                           // 서버에 전송할 요청 데이터 객체
    playerId: playerId.value,                                                                     // 입력받은 플레이어 ID (.value로 ref 값 접근)
    playerPassword: playerPassword.value,                                                         // 입력받은 비밀번호 (.value로 ref 값 접근)
    playerMoney: 0                                                                                // 초기 자금을 0으로 설정
  }
  const response = await apiCall.post(url, null, requestBody)                                     // POST 요청으로 회원가입 시도 (응답 대기)
  console.log(response)                                                                           // 응답 내용을 콘솔에 출력 (디버깅용)

  if (response.result === 0) {                                                                    // 응답 결과가 성공(0)인지 확인
    isNewPlayer.value = false;                                                                    // 신규 사용자 플래그를 false로 설정 (로그인 버튼 표시)
  }
}



</script>

<!-- ===================================================================================================
     스타일 정의 영역 - 컴포넌트에만 적용되는 CSS (scoped)
     =================================================================================================== -->
<style scoped>
.bss-background {                                                                                 /* 배경 이미지를 적용할 클래스 정의 */
  width: 590px;                                                                                   /* 고정 너비 590픽셀 설정 */
  height: 380px;                                                                                  /* 고정 높이 380픽셀 설정 */
  background-image: url('/logo.png');                                                             /* 배경 이미지로 로고 파일 사용 */
  background-size: cover;                                                                         /* 배경 이미지를 컨테이너 전체에 맞게 확대/축소 */
  background-position: center;                                                                    /* 배경 이미지를 중앙에 위치 */
  background-repeat: no-repeat;                                                                   /* 배경 이미지 반복 방지 */
}
</style>
