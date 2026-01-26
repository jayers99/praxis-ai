Feature: Catalog artifact into research library
  As a researcher using Praxis
  I want to catalog research artifacts programmatically
  So that I can maintain the research library consistently

  Scenario: Successfully catalog a new artifact
    Given a research artifact with valid metadata at "_workshop/1-inbox/my-topic-research.md"
    And the research-library exists at "research-library/"
    When I catalog the artifact to topic "patterns"
    Then the artifact is moved to "research-library/patterns/my-topic-research.md"
    And the CATALOG.md Quick Reference table contains the artifact
    And the CATALOG.md By Topic section under "patterns" contains the artifact
    And the CATALOG.md By Consensus section contains the artifact
    And the CATALOG.md Keyword Index contains entries for each keyword
    And the CATALOG.md Recently Added section contains the artifact at the top

  Scenario: Reject artifact with missing required metadata
    Given a research artifact missing the "id" field
    When I validate the artifact metadata
    Then validation returns an error for "id: required field missing"

  Scenario: Reject artifact with duplicate ID
    Given an artifact with id "patterns-my-research-2026-01-04" exists in CATALOG.md
    And a new artifact has the same id "patterns-my-research-2026-01-04"
    When I catalog the new artifact
    Then cataloging fails with error "duplicate ID: patterns-my-research-2026-01-04"

  Scenario: Auto-create topic folder if missing
    Given a research artifact with valid metadata
    And no "research-library/new-topic/" folder exists
    When I catalog the artifact to topic "new-topic"
    Then the folder "research-library/new-topic/" is created
    And the artifact is cataloged successfully

  Scenario: Detect orphan artifacts
    Given an artifact exists at "research-library/patterns/orphan.md"
    And the artifact is not listed in CATALOG.md
    When I run orphan detection
    Then "patterns/orphan.md" is returned in the orphan list

  Scenario: Reindex library produces consistent catalog
    Given a research library with 5 artifacts
    When I reindex the library twice
    Then both runs produce identical CATALOG.md content
