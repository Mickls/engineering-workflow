#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"

module AgentMetadataValidator
  MAX_DEFAULT_PROMPT_CHARS = 180
  SENTENCE_TERMINATORS = /[。！？!?]|[.](?=\s|\z)/

  def self.validate(skill_root)
    errors = []
    paths = Dir[File.join(skill_root, "*", "agents", "openai.yaml")].sort
    errors << "#{skill_root}: no agents/openai.yaml files found" if paths.empty?

    paths.each do |path|
      skill_name = File.basename(File.dirname(File.dirname(path)))
      begin
        payload = YAML.safe_load(
          File.read(path, encoding: "UTF-8"),
          permitted_classes: [],
          aliases: false,
          filename: path
        )
      rescue Psych::Exception, SystemCallError => e
        errors << "#{path}: unable to parse YAML: #{e.message}"
        next
      end

      interface = payload.is_a?(Hash) ? payload["interface"] : nil
      prompt = interface.is_a?(Hash) ? interface["default_prompt"] : nil
      unless prompt.is_a?(String) && !prompt.strip.empty?
        errors << "#{path}: interface.default_prompt must be a non-empty string"
        next
      end

      errors << "#{path}: default_prompt must be a single line" if prompt.include?("\n")
      if prompt.length > MAX_DEFAULT_PROMPT_CHARS
        errors << "#{path}: default_prompt has #{prompt.length} characters; keep it at #{MAX_DEFAULT_PROMPT_CHARS} or less"
      end
      unless prompt.include?("$#{skill_name}")
        errors << "#{path}: default_prompt must mention $#{skill_name}"
      end
      if prompt.scan(SENTENCE_TERMINATORS).length > 1
        errors << "#{path}: default_prompt must contain one main sentence"
      end
    end

    [errors, paths.length]
  end
end

if $PROGRAM_NAME == __FILE__
  root = ARGV.fetch(0, "plugins/engineering-workflow/skills")
  errors, count = AgentMetadataValidator.validate(root)
  unless errors.empty?
    warn errors.join("\n")
    exit 1
  end
  puts "validated #{count} skill agent prompts"
end
