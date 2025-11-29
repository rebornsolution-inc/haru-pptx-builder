# Pretendard 폰트 설치 가이드

## 다운로드

1. **Pretendard 공식 GitHub 릴리즈 페이지 방문:**
   https://github.com/orioncactus/pretendard/releases

2. **최신 버전의 TTF 파일 다운로드:**
   - `Pretendard-X.X.X.zip` 다운로드
   - 압축 해제 후 `public/static` 폴더 내 TTF 파일 확인

3. **필요한 파일만 이 폴더에 복사:**
   ```
   fonts/
   ├── Pretendard-Regular.ttf    (일반)
   ├── Pretendard-Medium.ttf      (중간)
   ├── Pretendard-SemiBold.ttf    (세미볼드)
   └── Pretendard-Bold.ttf        (볼드)
   ```

## 빠른 설치 (PowerShell)

```powershell
# 1. 임시 폴더에 다운로드
$url = "https://github.com/orioncactus/pretendard/releases/latest/download/Pretendard-1.3.9.zip"
$zipPath = "$env:TEMP\Pretendard.zip"
$extractPath = "$env:TEMP\Pretendard"

Invoke-WebRequest -Uri $url -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force

# 2. 필요한 TTF 파일만 복사
$fontsDir = ".\fonts"
Copy-Item "$extractPath\public\static\Pretendard-Regular.ttf" $fontsDir
Copy-Item "$extractPath\public\static\Pretendard-Medium.ttf" $fontsDir
Copy-Item "$extractPath\public\static\Pretendard-SemiBold.ttf" $fontsDir
Copy-Item "$extractPath\public\static\Pretendard-Bold.ttf" $fontsDir

# 3. 정리
Remove-Item $zipPath, $extractPath -Recurse -Force
```

## 확인

다운로드 후 이 폴더에 최소한 아래 파일들이 있어야 합니다:
- ✅ `Pretendard-Regular.ttf`
- ✅ `Pretendard-Bold.ttf`

## 라이선스

Pretendard는 **SIL Open Font License 1.1**로 배포됩니다.
상업적 사용 가능하며, 자유롭게 사용/수정/배포할 수 있습니다.

자세한 내용: https://github.com/orioncactus/pretendard
