# frozen_string_literal: true

require "minitest/autorun"
require "tmpdir"
require "fileutils"
require_relative "../scripts/validate-agent-metadata"

class ValidateAgentMetadataTest < Minitest::Test
  def with_skill(prompt)
    Dir.mktmpdir do |root|
      agents = File.join(root, "test-skill", "agents")
      FileUtils.mkdir_p(agents)
      File.write(
        File.join(agents, "openai.yaml"),
        <<~YAML
          interface:
            display_name: "Test"
            short_description: "Test skill metadata"
            default_prompt: #{prompt.inspect}
        YAML
      )
      yield root
    end
  end

  def test_accepts_short_prompt_with_skill_name
    with_skill("Use $test-skill to test metadata.") do |root|
      errors, count = AgentMetadataValidator.validate(root)
      assert_equal 1, count
      assert_empty errors
    end
  end

  def test_rejects_missing_skill_name
    with_skill("Test metadata.") do |root|
      errors, = AgentMetadataValidator.validate(root)
      assert errors.any? { |error| error.include?("must mention $test-skill") }
    end
  end

  def test_rejects_long_prompt
    prompt = "$test-skill #{'x' * AgentMetadataValidator::MAX_DEFAULT_PROMPT_CHARS}"
    with_skill(prompt) do |root|
      errors, = AgentMetadataValidator.validate(root)
      assert errors.any? { |error| error.include?("characters") }
    end
  end

  def test_rejects_multiple_sentences
    with_skill("Use $test-skill. Then do more.") do |root|
      errors, = AgentMetadataValidator.validate(root)
      assert errors.any? { |error| error.include?("one main sentence") }
    end
  end
end
