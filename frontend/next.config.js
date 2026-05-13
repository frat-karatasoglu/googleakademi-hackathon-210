/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      { source: '/demo', destination: '/demo.html' },
    ]
  },
}

module.exports = nextConfig
