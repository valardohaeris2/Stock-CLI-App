/**
 * @type {import('semantic-release').GlobalConfig}
 */
module.exports = {
  branches: ["main"],
  plugins: [
    [
      "@semantic-release/git",
      {
        assets: ["dist/*.js", "dist/*.js.map"],
        message:
          "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes",
      },
    ],
  ],
};
