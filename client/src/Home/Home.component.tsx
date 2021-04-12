import React, { useState } from "react";
import ActionSwitch from "./ActionSwitch/ActionSwitch.component";
import ActionContainer from "./ActionContainer/ActionContainer.component";
import { Container } from "@material-ui/core";
import { APIEndpointUrl } from "./APIEndpoint";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      marginTop: theme.spacing(5),
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
    },
  })
);

export default function Home() {
  const classes = useStyles();

  const [APIUrl, setAPIUrl] = useState<string>(APIEndpointUrl.ADD_TRANSACTION);

  return (
    <Container maxWidth="sm" className={classes.root}>
      <ActionSwitch setAPIUrl={setAPIUrl} />
      <ActionContainer APIUrl={APIUrl} />
    </Container>
  );
}
