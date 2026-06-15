// 성서유니온(sum.su.or.kr:8888) 전용 얇은 프록시.
//
// 배경: GitHub Actions(Azure) egress IP가 union 서버에 간헐적으로 차단된다.
// Deno Deploy는 비-Azure 네트워크 + 임의 포트(8888) outbound를 허용하므로,
// GitHub Actions -> 이 프록시 -> union 순으로 호출하면 차단을 우회한다.
//
// 배포: https://dash.deno.com 에서 새 Playground/Project 생성 후 이 파일 내용을
// 붙여넣고, 환경변수 PROXY_TOKEN 에 임의의 시크릿 문자열을 설정한다.
//
// 보안: 오픈 릴레이 방지를 위해 x-proxy-token 헤더가 PROXY_TOKEN과 일치할 때만
// 동작한다. 업스트림은 union으로 고정되어 임의 URL 프록시로 악용될 수 없다.

const UPSTREAM = "https://sum.su.or.kr:8888";
const TOKEN = Deno.env.get("PROXY_TOKEN");

Deno.serve(async (req: Request): Promise<Response> => {
  const url = new URL(req.url);

  // 헬스체크용
  if (url.pathname === "/" || url.pathname === "/health") {
    return new Response("ok", { status: 200 });
  }

  // 공유 토큰 검증
  if (!TOKEN || req.headers.get("x-proxy-token") !== TOKEN) {
    return new Response("forbidden", { status: 403 });
  }

  // union의 /Ajax/... 경로만 그대로 전달 (쿼리는 무시, union은 POST 본문 사용)
  const target = UPSTREAM + url.pathname;
  try {
    const upstream = await fetch(target, {
      method: req.method,
      headers: {
        "content-type":
          req.headers.get("content-type") ??
          "application/x-www-form-urlencoded",
      },
      body:
        req.method === "GET" || req.method === "HEAD"
          ? undefined
          : await req.arrayBuffer(),
    });

    return new Response(await upstream.arrayBuffer(), {
      status: upstream.status,
      headers: {
        "content-type":
          upstream.headers.get("content-type") ?? "application/json",
      },
    });
  } catch (err) {
    return new Response(`upstream error: ${err}`, { status: 502 });
  }
});
