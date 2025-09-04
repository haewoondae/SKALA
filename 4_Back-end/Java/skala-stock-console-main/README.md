# SKALA STOCK Console

### 자동 저장 기능 설정

.vscode/settings.json

```json
{
	"java.project.sourcePaths": ["src"],
	"java.project.outputPath": "bin",
	"java.project.referencedLibraries": ["lib/**/*.jar"], // 저장시 이벤트 설정 추가
	"java.format.settings.url": "eclipse-formatter.xml",
	"editor.formatOnSave": true, // 저장할 때 코드 포맷 자동 정리
	"editor.codeActionsOnSave": {
		"source.organizeImports": "always" // 필요한 클래스 import 문장 자동 추가/삭제
	},
	"[java]": {
		"editor.tabSize": 4, // 탭 크기 설정 (기본값 4)
		"editor.insertSpaces": true, // 탭 대신 공백 사용
		"editor.formatOnSave": true // 저장 시 자동 포맷팅
	}
}
```

### 터미널에서 실행하기

```shell
# 컴파일
javac -d bin src/*.java

# 실행
java  -cp bin App
```
