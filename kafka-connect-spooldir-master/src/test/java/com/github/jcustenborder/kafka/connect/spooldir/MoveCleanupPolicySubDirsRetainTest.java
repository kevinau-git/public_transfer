package com.github.jcustenborder.kafka.connect.spooldir;

import org.junit.jupiter.api.Test;

import com.google.common.collect.ImmutableMap;

import java.io.File;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class MoveCleanupPolicySubDirsRetainTest extends MoveCleanupPolicyTest {

  @Override
  protected String defineInputPathSubDir() {
    return "test/01/02/03";
  }

  protected ImmutableMap.Builder<String,String> getConnectorConfigMap() {
    return super.getConnectorConfigMap()
      .put(SpoolDirBinaryFileSourceConnectorConfig.INPUT_PATH_WALK_RECURSIVELY, "true")
      .put(SpoolDirBinaryFileSourceConnectorConfig.CLEANUP_POLICY_MAINTAIN_RELATIVE_PATH, "true");
  }

  @Test
  public void success() throws IOException {
    super.success();

    assertTrue(new File(this.inputPath,this.defineInputPathSubDir()).exists(), 
      "The input.path sub-directory "+this.defineInputPathSubDir()+" should exist");

  }
}
