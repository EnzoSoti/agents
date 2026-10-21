#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function getTargetProjectRoot() {
  if (process.env.INIT_CWD) {
    return process.env.INIT_CWD;
  }
  const parts = __dirname.split(path.sep);
  const nmIndex = parts.lastIndexOf('node_modules');
  if (nmIndex !== -1) {
    return parts.slice(0, nmIndex).join(path.sep);
  }
  return process.cwd();
}

function copyFolderSync(source, target, options = { overwrite: true }) {
  if (!fs.existsSync(target)) {
    fs.mkdirSync(target, { recursive: true });
  }

  const items = fs.readdirSync(source, { withFileTypes: true });

  for (const item of items) {
    const srcPath = path.join(source, item.name);
    const destPath = path.join(target, item.name);

    if (item.isDirectory()) {
      copyFolderSync(srcPath, destPath, options);
    } else {
      if (!options.overwrite && fs.existsSync(destPath)) {
        // Skip existing file to protect user modifications
        continue;
      }
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function getAvailableSkills(skillsDir) {
  if (!fs.existsSync(skillsDir)) return [];
  return fs
    .readdirSync(skillsDir, { withFileTypes: true })
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);
}

function printUsage() {
  console.log(`
@enzosoti/agents CLI

Usage:
  npx agents [command] [options]

Commands:
  install, add <skill...>   Install specific skill(s) or all if none specified
  install --all             Install all available skills
  update                    Pull latest changes and sync updated skills
  list                      List all available agent skills
  link [--cursor] [--claude] Generate IDE agent pointers (.cursorrules, CLAUDE.md)
  help                      Show this help message

Options:
  --force, -f               Overwrite existing files without prompting
  --skip-existing           Preserve existing files in target project (default in postinstall)
  --dest <dir>              Specify custom installation destination directory
`);
}

function run() {
  const args = process.argv.slice(2);
  const packageRoot = path.resolve(__dirname, '..');
  const sourceAgentsDir = path.join(packageRoot, '.agents');
  const sourceSkillsDir = path.join(sourceAgentsDir, 'skills');

  const targetProjectRoot = getTargetProjectRoot();
  const destAgentsDir = path.join(targetProjectRoot, '.agents');
  const destSkillsDir = path.join(destAgentsDir, 'skills');

  const command = args[0] || 'install';

  if (command === 'help' || command === '--help' || command === '-h') {
    printUsage();
    return;
  }

  const availableSkills = getAvailableSkills(sourceSkillsDir);

  if (command === 'list' || command === 'ls') {
    console.log('\nAvailable Agent Skills:');
    console.log('-----------------------');
    availableSkills.forEach((s, idx) => {
      console.log(`  ${String(idx + 1).padStart(2, ' ')}. ${s}`);
    });
    console.log(`\nTotal: ${availableSkills.length} skills\n`);
    console.log('Install with: npx agents add <skill-name>\n');
    return;
  }

  // Prevent self-copy if running install inside package source repo
  if (path.resolve(sourceAgentsDir) === path.resolve(destAgentsDir)) {
    console.log('[agents] Inside package root repository. Skipping copy.');
    return;
  }

  if (command === 'link') {
    const isCursor = args.includes('--cursor') || args.includes('-c') || (!args.includes('--claude') && !args.includes('-cl'));
    const isClaude = args.includes('--claude') || args.includes('-cl') || (!args.includes('--cursor') && !args.includes('-c'));

    if (isCursor) {
      const cursorRulesPath = path.join(targetProjectRoot, '.cursorrules');
      const cursorContent = `# AI Agent Skills\nAgent skills and instructions are available in \`.agents/skills/\`.\nRefer to \`.agents/skills/README.md\` for the active catalog.\n`;
      fs.writeFileSync(cursorRulesPath, cursorContent, 'utf8');
      console.log(`✅ Created ${cursorRulesPath}`);
    }

    if (isClaude) {
      const claudePath = path.join(targetProjectRoot, 'CLAUDE.md');
      const claudeContent = `# Claude Agent Instructions\n\nWhen working on this repository, consult operational skills located in \`.agents/skills/\`.\nPrimary orchestrator: \`.agents/skills/universal-dev-orchestrator/SKILL.md\`.\n`;
      fs.writeFileSync(claudePath, claudeContent, 'utf8');
      console.log(`✅ Created ${claudePath}`);
    }
    return;
  }

  const isForce = args.includes('--force') || args.includes('-f') || command === 'update';
  const isPostinstall = process.env.npm_lifecycle_event === 'postinstall';
  // If postinstall and not force, do not overwrite modified files
  const overwrite = isForce || !isPostinstall;

  let selectedSkills = [];

  if (command === 'add' || command === 'install') {
    const rawSkills = args.slice(1).filter((arg) => !arg.startsWith('-'));
    if (rawSkills.length > 0) {
      selectedSkills = rawSkills;
    }
  }

  if (selectedSkills.length > 0) {
    // Install specific skills
    console.log(`[agents] Installing selected skill(s) into: ${targetProjectRoot}...`);
    fs.mkdirSync(destSkillsDir, { recursive: true });

    for (const skill of selectedSkills) {
      if (!availableSkills.includes(skill)) {
        console.warn(`⚠️  [agents] Skill "${skill}" not found. Run 'npx agents list' to view available skills.`);
        continue;
      }
      const srcSkillDir = path.join(sourceSkillsDir, skill);
      const destSkillDir = path.join(destSkillsDir, skill);
      copyFolderSync(srcSkillDir, destSkillDir, { overwrite });
      console.log(`  ✓ Installed skill: ${skill}`);
    }

    // Also copy top-level manifest, README, and AGENTS.md rules if missing
    ['.antigravity-install-manifest.json', 'README.md'].forEach((file) => {
      const srcFile = path.join(sourceSkillsDir, file);
      const destFile = path.join(destSkillsDir, file);
      if (fs.existsSync(srcFile) && (!fs.existsSync(destFile) || overwrite)) {
        fs.copyFileSync(srcFile, destFile);
      }
    });

    const rootAgentsMd = path.join(packageRoot, 'AGENTS.md');
    const destAgentsMd = path.join(targetProjectRoot, 'AGENTS.md');
    if (fs.existsSync(rootAgentsMd) && (!fs.existsSync(destAgentsMd) || isForce)) {
      fs.copyFileSync(rootAgentsMd, destAgentsMd);
      console.log('  ✓ Installed AGENTS.md operating rules in project root');
    }

    console.log('✅ [agents] Done!');
  } else {
    // Install everything
    console.log(`[agents] Installing all agents & skills into: ${targetProjectRoot}...`);
    copyFolderSync(sourceAgentsDir, destAgentsDir, { overwrite });

    const rootAgentsMd = path.join(packageRoot, 'AGENTS.md');
    const destAgentsMd = path.join(targetProjectRoot, 'AGENTS.md');
    if (fs.existsSync(rootAgentsMd) && (!fs.existsSync(destAgentsMd) || isForce)) {
      fs.copyFileSync(rootAgentsMd, destAgentsMd);
      console.log('  ✓ Installed AGENTS.md operating rules in project root');
    }

    console.log(`✅ [agents] Successfully synchronized .agents folder to ${targetProjectRoot}`);
  }
}

try {
  run();
} catch (err) {
  console.error('❌ [agents] Error during execution:', err);
  process.exit(1);
}
