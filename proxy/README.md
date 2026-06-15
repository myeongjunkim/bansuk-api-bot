# union 프록시 (Deno Deploy)

GitHub Actions(Azure) egress IP가 성서유니온 서버(`sum.su.or.kr:8888`)에 간헐적으로
차단되는 문제를 우회하기 위한 얇은 프록시. 비-Azure 네트워크인 Deno Deploy에서
union을 대신 호출한다.

```
GitHub Actions ──> Deno Deploy 프록시 ──> sum.su.or.kr:8888
   (Azure)          (비-Azure, 포트 8888 OK)
```

## 배포 방법 (이 repo CI가 자동 배포)

프록시 코드 배포는 [`.github/workflows/deploy-proxy.yaml`](../.github/workflows/deploy-proxy.yaml)
가 담당한다. `proxy/union-proxy.ts` 가 main에 푸시되면 Deno Deploy로 자동 배포된다.

**사전 1회 설정(대시보드):**

1. <https://dash.deno.com> 접속 → GitHub 계정으로 로그인(무료).
2. **New Project** 생성. 프로젝트명은 `union-proxy` 로 한다
   (deploy-proxy.yaml 의 `project:` 값과 일치해야 함).
3. 배포 방식으로 **GitHub Actions** 선택 → 이 repo 연결(OIDC 신뢰 구성).
4. 프로젝트 **Settings → Environment Variables** 에 추가:
   - `PROXY_TOKEN` = 임의의 긴 랜덤 문자열 (예: `openssl rand -hex 24` 결과)
5. 이후 `proxy/union-proxy.ts` 푸시 시 CI가 자동 배포 → 배포 URL
   (예: `https://union-proxy-xxxx.deno.dev`) 확보.

## 배포 후 검증 (프록시가 union에 실제로 닿는지)

```bash
curl -X POST 'https://union-proxy-xxxx.deno.dev/Ajax/Bible/BodyTop' \
  -H 'x-proxy-token: <PROXY_TOKEN>' \
  --data "qt_ty=QT1&Base_de=$(date +%Y-%m-%d)"
```

→ union JSON(`BibleDay` 등)이 떨어지면 성공. `502 upstream error`면 Deno Deploy에서
union에 못 닿는 것이므로 다른 플랫폼(Vercel/GitLab CI)으로 전환 필요.

## GitHub에 연결

리포지토리 **Settings → Secrets and variables → Actions** 에 추가:

- `UNION_BASE_URL` = `https://union-proxy-xxxx.deno.dev`
- `UNION_PROXY_TOKEN` = 위 `PROXY_TOKEN`과 동일한 값

워크플로우의 `send message` 스텝이 이 둘을 환경변수로 전달하며, 설정되어 있으면
`bansuk_bot/clients/union.py`가 직접 호출 대신 프록시를 거친다. (미설정 시 직접 호출)
