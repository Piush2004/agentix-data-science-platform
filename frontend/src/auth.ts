import { NextRequest, NextResponse } from "next/server";

// Mock session representing the default logged-in enterprise admin
export const mockSession = {
  user: {
    id: "default-user",
    name: "Enterprise Admin",
    email: "admin@agentix.com",
    role: "ADMIN"
  },
  expires: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
};

// auth function returned by NextAuth, used in API routes and server components
export async function auth() {
  return mockSession;
}

// signIn and signOut functions for components
export async function signIn() {
  return true;
}

export async function signOut() {
  return true;
}

// Route handlers for NextAuth endpoint (/api/auth/session etc.)
async function handleAuth(req: NextRequest) {
  const url = new URL(req.url);
  const pathname = url.pathname;

  if (pathname.includes("/session")) {
    return NextResponse.json(mockSession);
  }
  
  if (pathname.includes("/csrf")) {
    return NextResponse.json({ csrfToken: "mock-csrf-token" });
  }

  if (pathname.includes("/providers")) {
    return NextResponse.json({
      credentials: {
        id: "credentials",
        name: "Credentials",
        type: "credentials",
        signinUrl: "/api/auth/signin/credentials",
        callbackUrl: "/dashboard"
      }
    });
  }

  // Fallback for signin, signout, callback, etc.
  return NextResponse.json({ success: true });
}

export const handlers = {
  GET: handleAuth,
  POST: handleAuth
};
