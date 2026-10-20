#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function copyFolderSync(source, target) {
  if (!fs.existsSync(target)) {
    fs.mkdirSync(target, { recursive: true });
  }

  const items = fs.readdirSync(source, { withFileTypes: true });

  for (const item of items) {
    const srcPath = path.join(source, item.name);
    const destPath = path.join(target, item.name);

    if (item.isDirectory()) {
      copyFolderSync(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function getTargetProjectRoot() {
  // 1. If INIT_CWD is set by npm/yarn/pnpm, that is the directory where `npm install` was run
  if (process.env.INIT_CWD) {
    return process.env.INIT_CWD;
  }

  // 2. If installed as a dependency inside node_modules/@enzosoti/agents or node_modules/agents
  // __dirname: <project_root>/node_modules/<pkg>/bin -> go up 3 or 4 levels
  const parts = __dirname.split(path.sep);
  const nmIndex = parts.lastIndexOf('node_modules');
  if (nmIndex !== -1) {
    return parts.slice(0, nmIndex).join(path.sep);
  }

  // 3. Fallback to process.cwd()
  return process.cwd();
}

function install() {
  const packageRoot = path.resolve(__dirname, '..');
  const sourceAgentsDir = path.join(packageRoot, '.agents');
  const targetProjectRoot = getTargetProjectRoot();
  const destAgentsDir = path.join(targetProjectRoot, '.agents');

  // Avoid copying into itself if installing inside the package directory
  if (path.resolve(sourceAgentsDir) === path.resolve(destAgentsDir)) {
    console.log('[agents] Source and destination are identical. Skipping copy.');
    return;
  }

  if (!fs.existsSync(sourceAgentsDir)) {
    console.warn(`[agents] Source .agents directory not found at ${sourceAgentsDir}`);
    return;
  }

  try {
    console.log(`[agents] Installing .agents into: ${targetProjectRoot}...`);
    copyFolderSync(sourceAgentsDir, destAgentsDir);
    console.log('✅ [agents] Successfully copied .agents folder to your project codebase!');
  } catch (err) {
    console.error('❌ [agents] Error copying .agents folder:', err);
  }
}

install();
